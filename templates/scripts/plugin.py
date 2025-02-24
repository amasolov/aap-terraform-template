import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from typing import Any
from netaddr import IPNetwork

import makejinja
import validation
import re
import json


# Return the filename of a path without the j2 extension
def basename(value: str) -> str:
    return Path(value).stem


# Return the nth host in a CIDR range
def nthhost(value: str, query: int) -> str:
    value = IPNetwork(value)
    try:
        nth = int(query)
        if value.size > nth:
            return str(value[nth])
    except ValueError:
        return False
    return value


# Return the age public key from age.key
def age_public_key() -> str:
    try:
        with open('age.key', 'r') as file:
            file_content = file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: age.key") from e
    key_match = re.search(r"# public key: (age1[\w]+)", file_content)
    if not key_match:
        raise ValueError("Could not find public key in age.key")
    return key_match.group(1)

# Return the age private key from age.key
def age_private_key() -> str:
    try:
        with open('age.key', 'r') as file:
            file_content = file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: age.key") from e
    key_match = re.search(r"(AGE-SECRET-KEY-[\w]+)", file_content)
    if not key_match:
        raise ValueError("Could not find private key in age.key")
    return key_match.group(1)

# Return the GitHub deploy key from deploy.key
def deploy_key() -> str:
    try:
        with open('deploy.key', 'r') as file:
            file_content = file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: deploy.key") from e
    return file_content

# Return the ssh key from the provided path
def ssh_key(value: str) -> str:
    try:
        with open(value, 'r') as file:
            file_content = file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"SSH Key file not found") from e
    return file_content

def import_filter(file: Path) -> Callable[[dict[str, Any]], bool]:
    module_path = file.relative_to(Path.cwd()).with_suffix("")
    module_name = str(module_path).replace("/", ".")
    spec = importlib.util.spec_from_file_location(module_name, file)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.main


class Plugin(makejinja.plugin.Plugin):
    def __init__(self, data: dict[str, Any], config: makejinja.config.Config):
        self._data = data
        self._config = config

        self._excluded_dirs: set[Path] = set()
        for input_path in config.inputs:
            for filter_file in input_path.rglob(".mjfilter.py"):
                filter_func = import_filter(filter_file)
                if filter_func(data) is False:
                    self._excluded_dirs.add(filter_file.parent)

        validation.validate(data)


    def filters(self) -> makejinja.plugin.Filters:
        return [
            basename,
            nthhost
        ]


    def functions(self) -> makejinja.plugin.Functions:
        return [
            age_private_key,
            age_public_key,
            deploy_key,
            ssh_key
        ]


    def path_filters(self):
        return [
            self._mjfilter_func
        ]


    def _mjfilter_func(self, path: Path) -> bool:
        return not any(
            path.is_relative_to(excluded_dir) for excluded_dir in self._excluded_dirs
        )
