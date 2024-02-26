from pathlib import Path

import pytest

import tibian
import tibian.config as tc


@pytest.fixture
def _example_config_file():
    yield Path(__file__).parent.parent / "config.example.yaml"


def test_load_config(_example_config_file):
    config = tc.load_config(_example_config_file)

    assert config is not None
    assert "sources" in config
    assert "destinations" in config


@pytest.mark.parametrize(
    "entry_type, possibles, resulttype",
    [
        ("jira", tibian.sources.POSSIBLE_SOURCES, tibian.sources.jira.JiraSource),
        ("stdout", tibian.targets.POSSIBLE_DESTINATIONS, tibian.targets.stdout.StdoutTarget),
    ],
)
def test_get_cls_from_possible(entry_type, possibles, resulttype):
    assert tc.get_cls_from_possible(entry_type, possibles) == resulttype


def test_get_cls_from_possible__invalid_type__raises_valueerror(mocker):
    with pytest.raises(ValueError):
        tc.get_cls_from_possible("nonexistent", [])


def test_construct_objects_based_on_config_type(_example_config_file, mocker):
    config = tc.load_config(_example_config_file)
    objs = tc.construct_objects_based_on_config_type(config["destinations"])

    assert objs is not None
    assert len(objs) == 2
    assert isinstance(objs[0], tibian.targets.stdout.StdoutTarget)
    assert isinstance(objs[1], tibian.targets.teams.TeamsTarget)

    stdout = objs[0]
    assert stdout.name == "my-console"

    teams = objs[1]
    assert teams.name == "my-teams-channel"
    assert teams.url == "https://company.webhook.office.com/webhookb2/abcde12f-..."
