import abc


class TicketSource(abc.ABC):

    TYPENAME = "unknown"

    def __init__(self, name: str, config: dict, *args, **kwargs) -> None:
        super().__init__()
        self.name = name

    @abc.abstractmethod
    def get_open_tickets(self):
        pass
