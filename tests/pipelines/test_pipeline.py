"""
    Module containing tests for the `Pipeline` class
"""

import pathlib

import pytest

from mindpipe.pipelines import Pipeline


@pytest.mark.usefixtures("example_pipelines")
class TestPipeline:
    """ Tests for the `Pipeline` class """

    def test_pipeline_init(self, example_pipeline_files):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        assert Pipeline(user_settings, profile="local")

    def test_pipeline_len_getitem(self, example_pipeline_files):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        pipeline = Pipeline(user_settings, profile="local")
        assert len(pipeline) == 4
        process = pipeline["make_json_network"]
        assert process.name == "make_json_network"

    def test_pipeline_run(self, example_pipeline_files, tmpdir):
        user_settings = example_pipeline_files["grouptaxa_sparcc_json"]
        pipeline_dir = tmpdir.mkdir("test_pipeline")
        input_dir = pathlib.Path.cwd() / "tests/data"
        pipeline = Pipeline(
            user_settings,
            profile="local",
            output_location=pipeline_dir,
            base_dir=input_dir,
        )
        for process in pipeline.run():
            process.wait()
            assert process.cmd.status == "success"
            for output in process.params.output:
                if "*" in str(output.location):
                    str_loc = str(output.location)
                    ind = str_loc.find("*")
                    files = list(pathlib.Path(str_loc[:ind]).glob(str_loc[ind:]))
                    assert len(files) > 0
                else:
                    assert output.location.exists()