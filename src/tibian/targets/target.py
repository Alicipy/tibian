import abc
from collections.abc import Sequence
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket


class Target(abc.ABC, BaseModel):
    name: str

    @abc.abstractmethod
    def announce_birthdays(self, birthday_tickets: Sequence["BirthdayTicket"]) -> None:
        pass
