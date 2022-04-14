from typing import TYPE_CHECKING, List

from tibian.targets.target import Target

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class StdoutTarget(Target):

    TYPENAME = "stdout"

    def __init__(self, name: str, config: dict, *args, **kwargs) -> None:
        super().__init__(name, config, *args, **kwargs)

    def announce_birthdays(self, birthday_tickets: List["BirthdayTicket"]) -> None:

        for bt in birthday_tickets:
            print(f"{bt.name} '{bt.title}': {bt.age}")
