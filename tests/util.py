from functools import singledispatch
from pathlib import Path

import io
from configparser import ConfigParser

import textwrap

from typing import Dict, Union, Any, Tuple

_CONFIG_FROM = Union[str, Path, io.IOBase, Dict[str, Dict[str, Any]], ConfigParser]


__all__ = ["generate_package", "compare_configs", "configs_to_str"]


def generate_package(root_path: Path, files: Dict[Union[str, Path], str]):
    """
    Given a root path and a dictionary mapping relative file paths to their
    contents, create the file hierarchy
    """
    for rel_path, contents in files.items():
        fpath = root_path / rel_path

        with open(fpath, "w") as f:
            f.write(textwrap.dedent(contents))


def compare_configs(cfg1: _CONFIG_FROM, cfg2: _CONFIG_FROM) -> ConfigParser:
    return _to_config(cfg1) == _to_config(cfg2)


def configs_to_str(*cfgs: ConfigParser) -> Tuple[str, ...]:
    return tuple(map(_config_to_str, cfgs))


def _config_to_str(cfg: ConfigParser) -> str:
    cfg = _to_config(cfg)

    s = io.StringIO()
    cfg.write(s)
    s.seek(0)
    return s.read()


@singledispatch
def _to_config(cfg):
    raise ValueError(f"Cannot convert to config file: {cfg!r}")


@_to_config.register(dict)
def _(cfg):
    cfg_out = ConfigParser()
    cfg_out.read_dict(cfg)
    return cfg_out


@_to_config.register(str)
def _(cfg):
    s = io.StringIO(cfg)
    return _to_config(s)


@_to_config.register(Path)
def _(cfg):
    with open(cfg, "r") as f:
        return _to_config(f)


@_to_config.register(io.IOBase)
def _(cfg):
    cfg_out = ConfigParser()
    cfg_out.read_file(cfg)

    return cfg_out


@_to_config.register(ConfigParser)
def _(cfg):
    return cfg
