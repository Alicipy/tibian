from pathlib import Path

import pytest

import tibian.config as tc
from tibian.sources.jira import JiraSource
from tibian.sources.taiga import TaigaSource
from tibian.targets.stdout import StdoutTarget
from tibian.targets.teams import TeamsTarget


@pytest.fixture
def _example_config_file():
    yield Path(__file__).parent.parent / "config.example.yaml"


def test_load_example_config(_example_config_file):
    config = tc.load_config(_example_config_file)

    assert config.sources is not None
    assert len(config.sources) == 2
    assert isinstance(config.sources[0], JiraSource)
    assert isinstance(config.sources[1], TaigaSource)

    assert config.destinations is not None
    assert len(config.destinations) == 2
    assert isinstance(config.destinations[0], StdoutTarget)
    assert isinstance(config.destinations[1], TeamsTarget)
