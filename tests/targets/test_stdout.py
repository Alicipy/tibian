import datetime
from unittest import mock

import tibian.vars
from tibian.targets.stdout import StdoutTarget
from tibian.tickets import BirthdayTicket


class TestStdoutTarget:
    def test_correct_initialization(self):
        stdout = StdoutTarget(name="stdout_name")
        assert stdout.name == "stdout_name"

    def test_get_open_tickets(self, capsys):
        tibian.vars.get_today = mock.Mock(return_value=datetime.date(2022, 3, 1))

        birthday_tickets = [
            BirthdayTicket("A", "ABC Ticket subscription", "open", datetime.date(2021, 3, 1)),
            BirthdayTicket("B", "ABC Ticket subscription", "open", datetime.date(2019, 3, 1)),
        ]

        stdout = StdoutTarget(name="stdout_name", type="stdout")
        stdout.announce_birthdays(birthday_tickets)

        captured = capsys.readouterr()

        assert captured.out.splitlines() == [
            "A 'ABC Ticket subscription': 1",
            "B 'ABC Ticket subscription': 3",
        ]
