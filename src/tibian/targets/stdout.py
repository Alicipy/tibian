from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from tibian.targets.target import Target

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class StdoutTarget(Target):
    type: Literal["stdout"] = "stdout"

    def announce_birthdays(self, birthday_tickets: Sequence["BirthdayTicket"]) -> None:
        for bt in birthday_tickets:
            print(f"{bt.name} '{bt.title}': {bt.age}")
