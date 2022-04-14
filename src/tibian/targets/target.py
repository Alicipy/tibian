import abc
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class Target(abc.ABC):

    TYPENAME = "unknown"

    def __init__(self, name: str, config: dict, *args, **kwargs) -> None:
        super().__init__()
        self.name = name

    @abc.abstractmethod
    def announce_birthdays(self, birthday_tickets: List["BirthdayTicket"]) -> None:
        pass
