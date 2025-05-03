import datetime

import pytest
from pydantic import HttpUrl

from tibian.targets.teams import TeamsTarget
from tibian.tickets import BirthdayTicket


@pytest.fixture
def teams_target_mock():
    yield TeamsTarget(
        name="teams_name",
        url="https://company.webhook.office.com/webhookb2/abcde12f-...",
    )


class TestTeamsTarget:
    def test_correct_initialization(self, teams_target_mock):
        assert teams_target_mock.name == "teams_name"
        assert teams_target_mock.url == HttpUrl(
            "https://company.webhook.office.com/webhookb2/abcde12f-..."
        )

    def test_get_open_tickets__it_is_some_tickets_birthday(self, teams_target_mock, requests_mock):
        birthday_tickets = [
            BirthdayTicket("A", "ABC Ticket subscription", "open", datetime.date(2021, 3, 1)),
            BirthdayTicket("B", "ABC Ticket subscription", "open", datetime.date(2019, 3, 1)),
        ]

        teams = teams_target_mock
        requests_mock.post(str(teams.url))

        teams.announce_birthdays(birthday_tickets)

        history = requests_mock.request_history[0]
        assert history.method == "POST"
        assert history.url == str(teams.url)
        assert history.json() is not None
        assert history.json()["sections"][0]["facts"] == [
            {"name": "A", "value": "ABC Ticket subscription (1 year(s))"},
            {"name": "B", "value": "ABC Ticket subscription (3 year(s))"},
        ]
        assert history.json()["sections"][0]["text"] == ""

    def test_get_open_tickets__it_is_no_tickets_birthday(self, requests_mock, teams_target_mock):
        birthday_tickets = []
        teams = teams_target_mock
        requests_mock.post(str(teams.url))

        teams.announce_birthdays(birthday_tickets)

        history = requests_mock.request_history[0]

        assert history.json()["sections"][0]["facts"] == []
        assert history.json()["sections"][0]["text"] == "**It's no tickets birthday today :(**"
