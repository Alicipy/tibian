import datetime

import pytest

from tibian.sources.jira import JiraSource
from tibian.tickets import Ticket


@pytest.fixture
def jira_source():
    yield JiraSource(
        name="jira_name",
        url="https://jira_url",
        project="jira_project",
        auth={"username": "jira_username", "password": "jira_password"},
    )


class TestJiraSource:
    def test_correct_initialization(self, jira_source):
        assert jira_source.name == "jira_name"
        assert jira_source.project == "jira_project"

    def test_get_open_tickets(self, jira_source, requests_mock):
        requests_mock.get(
            "https://jira_url/rest/api/3/search/jql",
            [
                {
                    "json": {
                        "issues": [
                            {
                                "key": "ABC-123",
                                "fields": {
                                    "status": {"name": "Open"},
                                    "summary": "ABC Ticket subscription",
                                    "created": "2020-01-01",
                                },
                            },
                            {
                                "key": "ABC-456",
                                "fields": {
                                    "status": {"name": "Implement"},
                                    "summary": "ABC Ticket subscription 2",
                                    "created": "2021-02-03",
                                },
                            },
                        ],
                        "nextPageToken": "hehe",
                    },
                    "status_code": 200,
                },
                {
                    "json": {
                        "issues": [
                            {
                                "key": "ABC-789",
                                "fields": {
                                    "status": {"name": "Open"},
                                    "summary": "ABC Ticket subscription 3",
                                    "created": "2022-04-05",
                                },
                            },
                        ],
                    },
                    "status_code": 200,
                },
            ],
        )

        tickets = jira_source.get_open_tickets()

        assert tickets == [
            Ticket("ABC-123", "ABC Ticket subscription", "Open", datetime.date(2020, 1, 1)),
            Ticket(
                "ABC-456",
                "ABC Ticket subscription 2",
                "Implement",
                datetime.date(2021, 2, 3),
            ),
            Ticket(
                "ABC-789",
                "ABC Ticket subscription 3",
                "Open",
                datetime.date(2022, 4, 5),
            ),
        ]
