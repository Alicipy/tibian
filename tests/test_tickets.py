import datetime
from unittest import mock

import pytest

import tibian.vars
from tibian.tickets import (
    BirthdayTicket,
    Ticket,
    announce_birthdays,
    collect_open_tickets,
    filter_for_birthday_tickets,
)


class TestTickets:
    def test_ticket_construction(self):
        Ticket("A", "ABC Ticket subscription", "open", datetime.date(2019, 2, 1))

    def test_ticket__is_tickets_birthday__is_tickets_birthday(self):
        tibian.vars.get_today = mock.Mock(return_value=datetime.date(2022, 3, 1))
        t = Ticket("A", "ABC Ticket subscription", "open", datetime.date(2019, 3, 1))
        assert t.is_tickets_birthday()

    @pytest.mark.parametrize(
        "day_of_ticket",
        [
            datetime.date(2022, 3, 1),
            datetime.date(2021, 2, 1),
            datetime.date(2021, 3, 2),
        ],
    )
    def test_ticket__is_tickets_birthday__is_not_tickets_birthday(self, day_of_ticket):
        tibian.vars.get_today = mock.Mock(return_value=datetime.date(2022, 3, 1))
        t = Ticket("A", "ABC Ticket subscription", "open", day_of_ticket)
        assert not t.is_tickets_birthday()

    def test_birthday_construction(self):
        BirthdayTicket("B", "DEF Ticket birthday", "open", datetime.date(2018, 4, 3))

    def test_birthday_ticket__age_correctly_calculated(self):
        tibian.vars.get_today = mock.Mock(return_value=datetime.date(2022, 3, 1))
        t = BirthdayTicket("B", "DEF Ticket birthday", "open", datetime.date(2018, 3, 1))
        assert t.age == 4

    def test_filter_for_birthday_tickets(self):

        tibian.vars.get_today = mock.Mock(return_value=datetime.date(2022, 3, 1))

        tickets = [
            Ticket("A", "ABC test ticket opened a year ago", "open", datetime.date(2021, 3, 1)),
            Ticket("B", "ABC test ticket opened today", "open", datetime.date(2022, 3, 1)),
            Ticket("C", "ABC test ticket not on this day", "open", datetime.date(2021, 4, 2)),
            Ticket("D", "ABC test ticket not on this month", "open", datetime.date(2021, 5, 1)),
        ]

        expected = [
            BirthdayTicket(
                "A", "ABC test ticket opened a year ago", "open", datetime.date(2021, 3, 1)
            ),
        ]

        result = filter_for_birthday_tickets(tickets)

        assert expected == result, tibian.vars.DAY

    def test_collect_open_tickets__two_sources__all_collected(self):
        t1 = [
            Ticket("A", "ABC test ticket opened a year ago", "open", datetime.date(2021, 3, 1)),
            Ticket("B", "ABC test ticket opened today", "open", datetime.date(2022, 3, 1)),
        ]
        t2 = [
            Ticket("C", "ABC test ticket not on this day", "open", datetime.date(2021, 4, 2)),
            Ticket("D", "ABC test ticket not on this month", "open", datetime.date(2021, 5, 1)),
        ]
        s1 = mock.Mock(get_open_tickets=mock.Mock(return_value=t1))
        s2 = mock.Mock(get_open_tickets=mock.Mock(return_value=t2))

        open_tickets = collect_open_tickets([s1, s2])

        assert open_tickets == t1 + t2

    def test_collect_open_tickets__no_sources(self):
        open_tickets = collect_open_tickets([])

        assert open_tickets == []

    def test_announce_birthdays__multiple_targets(self):

        ts = [mock.Mock(), mock.Mock()]
        birthday_tickets = [mock.Mock(), mock.Mock()]

        announce_birthdays(ts, birthday_tickets)

        for t in ts:
            t.announce_birthdays.assert_called_once_with(birthday_tickets)
