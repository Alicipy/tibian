import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class Target(abc.ABC):
    TYPENAME = "unknown"

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        super().__init__()
        self.name = name

    @abc.abstractmethod
    def announce_birthdays(self, birthday_tickets: list["BirthdayTicket"]) -> None:
        pass
