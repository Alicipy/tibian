from typing import Any, Union

import yaml
from pydantic import BaseModel

import tibian.vars
from tibian.sources.jira import JiraSource
from tibian.sources.taiga import TaigaSource
from tibian.targets.stdout import StdoutTarget
from tibian.targets.teams import TeamsTarget

_DEFAULT_CONFIG_PATH = tibian.vars.get_std_config_filepath()


class TibianConfig(BaseModel):
    sources: list[Union[JiraSource, TaigaSource]]
    destinations: list[Union[StdoutTarget, TeamsTarget]]


def load_config(filepath: str = _DEFAULT_CONFIG_PATH) -> TibianConfig:
    with open(filepath) as c:
        config: dict[str, Any] = yaml.safe_load(c)

    tibian_config = TibianConfig(**config)

    return tibian_config
