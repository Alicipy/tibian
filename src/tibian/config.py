from typing import Any, Dict, List, Sequence, Type, Union

import yaml

import tibian.vars
from tibian.sources import POSSIBLE_SOURCES
from tibian.sources.ticketsource import TicketSource
from tibian.targets import POSSIBLE_DESTINATIONS
from tibian.targets.target import Target

_DEFAULT_CONFIG_PATH = tibian.vars.get_std_config_filepath()


def load_config(filepath=_DEFAULT_CONFIG_PATH) -> Dict:

    with open(filepath) as c:
        config = yaml.safe_load(c)

    return config


def get_cls_from_possible(
    entry_type: str, possible: Sequence[Union[Type[TicketSource], Type[Target]]]
) -> Union[Type[TicketSource], Type[Target]]:

    for pos in possible:
        if pos.TYPENAME == entry_type:
            return pos

    raise ValueError(f"Couldn't find config class for type {entry_type}")


def _get_possible_classes() -> List[Union[Type[TicketSource], Type[Target]]]:

    possible_clss: List[Union[Type[TicketSource], Type[Target]]] = []
    possible_clss.extend(POSSIBLE_SOURCES)
    possible_clss.extend(POSSIBLE_DESTINATIONS)

    return possible_clss


def construct_objects_based_on_config_type(configs: Sequence[Dict[str, Any]]) -> Any:

    possible_clss = _get_possible_classes()

    objects = []
    for entry in configs:
        entry_type = entry["type"]
        cls = get_cls_from_possible(entry_type, possible_clss)
        obj = cls(entry["name"], entry["config"])
        objects.append(obj)

    return objects
