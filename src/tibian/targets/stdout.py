from typing import TYPE_CHECKING, Any

from tibian.targets.target import Target

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class StdoutTarget(Target):
    TYPENAME = "stdout"

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        super().__init__(name, config)

    def announce_birthdays(self, birthday_tickets: list["BirthdayTicket"]) -> None:
        for bt in birthday_tickets:
            print(f"{bt.name} '{bt.title}': {bt.age}")
