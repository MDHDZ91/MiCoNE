"""
    Module to parse and store pipeline settings
"""

import collections
import pathlib
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Set, Tuple, Union


PIPELINE_DIR = pathlib.Path(__file__).parent.parent / "pipelines"


class Input(NamedTuple):
    """ The namedtuple class for storing input """
    datatype: str
    format: List[str]  # noqa: E701
    location: Optional[pathlib.Path] = None

    def __hash__(self) -> int:
        return hash(self.datatype)


class Output(NamedTuple):
    """ The namedtuple class for storing output """
    datatype: str
    format: List[str]  # noqa: E701
    location: pathlib.Path

    def __hash__(self) -> int:
        return hash(self.datatype)


class Parameters(NamedTuple):
    """ The namedtuple class for storing proces parameters """
    process: str
    params: dict

    def __hash__(self) -> int:
        return hash(self.process)


IOType = Union[Input, Output]


class Params(collections.Hashable):
    """
        The class for parsing and storing the parameters of a process

        Parameters
        ----------
        data : Dict[str, Any]
            The information about the parameters for a particular process

        Attributes
        ----------
        name : str
            Process name
        root : pathlib.Path
            Root directory where the process pipeline is stored
        env : pathlib.Path
            Location of the virtual environment for the process
        output_location : pathlib.Path
            Directory relative to main output directory where results of the process are to be saved
        input : Set[Input]
            The list of inputs of the process
        output : Set[Output]
            The list of outputs of the process
        parameters : Set[Dict[str, Any]]
            The list of parameters of the process
    """
    _req_keys = {
        "root",
        "output_location",
        "input",
        "output",
        "parameters"
    }

    def __init__(self, data: Tuple[str, Dict[str, Any]]) -> None:
        if len(data) != 2:
            raise ValueError(f"Invalid process data: {data}")
        key, value = data
        for req_key in self._req_keys:
            if req_key not in value:
                raise ValueError(f"Invalid process data. {req_key} not found")
        self.name = key
        self.root = PIPELINE_DIR / value["root"]
        if not self.root.exists() or not self.root.is_dir():
            raise FileNotFoundError(
                f"The root directory: {self.root} doesn't exist. "
                "Please reinstall the package"
            )
        if "env" in value:
            self.env = PIPELINE_DIR / value["env"]
            if not self.env.exists() or not self.env.is_dir():
                raise FileNotFoundError(
                    f"The directory for the environment: {self.env} doesn't exist. "
                    "Please reinstall the package"
                )
        else:
            self.env = None
        self.output_location = pathlib.Path(value["output_location"])
        self.input = self._process_io(value["input"], "input")
        self.output = self._process_io(value["output"], "output")
        if not isinstance(value["parameters"], list):
            raise TypeError("Parameters must be a List.")
        self.parameters: Set[Parameters] = set()
        for curr_param in value["parameters"]:
            if "process" not in curr_param:
                raise ValueError("Parameters is missing 'process' field")
            params = {k: v for k, v in curr_param.items() if k != "process"}
            self.parameters.add(Parameters(process=curr_param["process"], params=params))

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        inputs = {i.datatype for i in self.input}
        outputs = {o.datatype for o in self.output}
        return f"<Params name={self.name} input={inputs} output={outputs}>"

    def __str__(self) -> str:
        return self.name

    def get(self, name: str, category: str) -> Union[Input, Output, Parameters]:
        """
            Get Input, Output or Parameter element using its name

            Parameters
            ----------
            name : str
                The name of the IO element or parameter to be retrieved
            category: {'input', 'output'}
                Specifies whether the data is input, output or parameter information

            Returns
            -------
            Union[Input, Output, Parameters]
                The Input, Output or Parameter element
        """
        if category == "input":
            query_set = self.input
            attr = "datatype"
        elif category == "output":
            query_set = self.output
            attr = "datatype"
        elif category == "parameters":
            query_set = self.parameters
            attr = "process"
        else:
            raise TypeError("Category can only be one of {'input', 'output', 'parameters'}")
        for element in query_set:
            if getattr(element, attr) == name:
                return element
        raise KeyError(f"{name} not found in {category} of {self.name}")

    @staticmethod
    def _process_io(data: List[Dict[str, Union[str, List[str]]]], category: str) -> Set[IOType]:
        """
            Process the input information

            Parameters
            ----------
            data : List[Dict[str, Union[str, List[str]]]]
                The input/output information
            category: {'input', 'output'}
                Specifies whether the data is input or output information

            Returns
            -------
            List[IOType]
                Processed input/output information
        """
        if category == "input":
            IO = Input
        elif category == "output":
            IO = Output
        else:
            raise TypeError("Category can only be either 'Input' or 'Output'")
        io_tuples: Set[IOType] = set()
        if not isinstance(data, list):
            raise TypeError(f"{category} must be a List")
        for item in data:
            req_fields = set(IO._fields) - set(IO._field_defaults.keys())
            for field in req_fields:
                if field not in item:
                    raise ValueError(f"Invalid {category}: {data}. Missing {field}")
            for field in item:
                if field not in IO._fields:
                    raise ValueError(f"Invalid {category}: {data}. Extra {field}")
            item_subset = {k: item[k] for k in req_fields}
            loc = item_subset.get("location")
            item_subset["location"] = pathlib.Path(loc) if loc else None
            io_tuples.add(IO(**item_subset))
        return io_tuples

    def update_location(self, name: str, location: str, category: str) -> None:
        """
            Update the location of an Input or Output element

            Parameters
            ----------
            name : str
                The name of the IO element whose location is to be updated
            location : str
                The location of the IO element
            category: {'input', 'output'}
                Specifies whether the data is input or output information
        """
        element = self.get(name, category=category)
        if category == "input":
            IO = Input
            io_list = self.input
        elif category == "output":
            IO = Output
            io_list = self.output
        else:
            raise TypeError("Category can only be either 'Input' or 'Output'")
        new_element = IO(
            datatype=element.datatype,
            format=element.format,
            location=location
        )
        io_list.remove(element)
        io_list.add(new_element)

    def verify_io(self) -> None:
        """
            Verify whether the Input and Output elements have been assigned and are valid
        """
        if not self.output_location.is_absolute():
            raise ValueError("The output location must be absolute")
        for elem in self.input:
            if elem.location is None:
                raise ValueError(f"Input: {elem} has not been assigned a location yet")
            if not elem.location.exists():
                raise FileNotFoundError(f"Unable to location input file at {elem.location}")
        for elem in self.output:
            if elem.location is None:
                raise ValueError(f"Output: {elem} has not been assigned a location yet")
            if not elem.location.is_absolute():
                raise ValueError("All the output objects do not have absolute paths")

    @property
    def dict(self) -> Dict[str, Any]:
        """
            Return data as a dictionary

            Returns
            -------
            Dict[str, Any]
                The data stored return as a dictionary
        """
        self.verify_io()
        data: Dict[str, Any] = dict()
        data["input"] = {elem.datatype: str(elem.location) for elem in self.input}
        data["output"] = {elem.datatype: str(elem.location) for elem in self.output}
        data["output_dir"] = self.output_location
        for process_params in self.parameters:
            data[process_params.process] = process_params.params
        return data

    def merge(self, user_settings: Dict[str, Any]) -> None:
        """
            Merge user_settings into the current Params instance

            Parameters
            ----------
            user_settings: Dict[str, Any]
                User defined settings for the current process
        """
        for curr_input in user_settings["input"]:
            io_item: Input = self.get(curr_input["datatype"], category="input")
            for f in curr_input["format"]:
                if f not in io_item.format:
                    raise ValueError(f"{f} not a supported format for {io_item}")
            updated_input = Input(
                datatype=io_item.datatype,
                format=curr_input["format"],
                location=curr_input["location"]
            )
            self.input.remove(io_item)
            self.input.add(updated_input)
        for curr_params in user_settings["parameters"]:
            param_item: Parameters = self.get(curr_params["process"], category="parameters")
            updated_param = Parameters(
                process=param_item.process,
                params={**param_item.params, **curr_params}
            )
            self.parameters.remove(param_item)
            self.parameters.add(updated_param)

    def attach_to(self, previous: "Params") -> None:
        """
            Update inputs of current `Param` instance using outputs of previous

            Parameters
            ----------
            previous : Params
                The `Param` instance to attach current instance to
        """
        for input_ in self.input:
            output_ = previous.get(input_.datatype, category="output")
            self.update_location(input_.datatype, output_.location, category="input")
        return None


class ParamsSet(collections.Set):
    """
        The set of all supported pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self.processes: Set[Params] = set()
        for key, value in data.items():
            process_params = Params((key, value))
            if process_params in self.processes:
                raise ValueError("Duplicate process definitions detected in settings. Aborting")
            self.processes.add(process_params)

    def __iter__(self) -> Iterator:
        return iter(self.processes)

    def __len__(self) -> int:
        return len(self.processes)

    def __contains__(self, value: str) -> bool:
        return value in [process.name for process in self.processes]

    def __getitem__(self, key: str) -> Params:
        for process in self.processes:
            if process.name == key:
                return process
        raise KeyError(f"{key} is not in ParamsSet")

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<ParamsSet n={len(self)} processes={processes}>"


class InternalParamsSet(ParamsSet):
    """
        The set of all supported internal pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the internal pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<InternalParamsSet n={len(self)} processes={processes}>"


class ExternalParamsSet(ParamsSet):
    """
        The set of all supported external pipeline processes

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary containing information about the external pipeline processes
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        data_processed = {}
        for level_1 in data:
            for level_2 in data[level_1]:
                for level_3 in data[level_1][level_2]:
                    name = f"{level_1}.{level_2}.{level_3}"
                    data_processed[name] = data[level_1][level_2][level_3]
        super().__init__(data_processed)

    def __repr__(self) -> str:
        processes = [process.name for process in self.processes]
        return f"<ExternalParamsSet n={len(self)} processes={processes}>"