import abc

from typing import Any

from tibian.tickets import Ticket


class TicketSource(abc.ABC):
    TYPENAME = "unknown"

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        super().__init__()
        self.name = name

    @abc.abstractmethod
    def get_open_tickets(self) -> list[Ticket]:
        pass
