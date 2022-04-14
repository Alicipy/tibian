import datetime
from dataclasses import astuple, dataclass
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from tibian.sources.ticketsource import TicketSource

import tibian.vars as tb_vars
from tibian.targets.target import Target


@dataclass
class Ticket:
    name: str
    title: str
    status: str
    creation_date: datetime.date

    def is_tickets_birthday(self) -> bool:
        day = tb_vars.get_today()
        a = day.replace(year=1) == self.creation_date.replace(year=1) and (
            day != self.creation_date
        )
        return a


@dataclass
class BirthdayTicket(Ticket):
    @property
    def age(self) -> int:
        return tb_vars.get_today().year - self.creation_date.year


def filter_for_birthday_tickets(open_tickets: List[Ticket]) -> List[BirthdayTicket]:
    return [BirthdayTicket(*astuple(t)) for t in open_tickets if t.is_tickets_birthday()]


def collect_open_tickets(sources: List["TicketSource"]):
    open_tickets = []
    for s in sources:
        tickets = s.get_open_tickets()
        open_tickets.extend(tickets)
    return open_tickets


def announce_birthdays(targets: List[Target], birthday_tickets: List[BirthdayTicket]) -> None:
    for target in targets:
        target.announce_birthdays(birthday_tickets)
