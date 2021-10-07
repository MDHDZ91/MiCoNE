#!/usr/bin/env python3

import pathlib
from typing import List

from micone import Network, NetworkGroup


def main(base_name: str, network_files: List[pathlib.Path]) -> None:
    networks: List[Network] = []
    for network_file in network_files:
        networks.append(Network.load_json(str(network_file)))
    network_group = NetworkGroup(networks)
    cids = [ctx["cid"] for ctx in network_group.contexts]
    merged_network_group = network_group.combine_pvalues(cids)
    merged_network_group.write(base_name + "_network.json", split_files=True)


if __name__ == "__main__":
    BASE_NAME = "${meta.id}"
    NETWORK_FILES = list(pathlib.Path().glob("*.json"))
    main(BASE_NAME, NETWORK_FILES)
