import abc


from pydantic import BaseModel

from tibian.tickets import Ticket


class TicketSource(abc.ABC, BaseModel):
    name: str

    @abc.abstractmethod
    def get_open_tickets(self) -> list[Ticket]:
        pass
