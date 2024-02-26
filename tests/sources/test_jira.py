import datetime
from unittest import mock

import pytest
from jira.client import Issue

from tibian.sources.jira import JiraSource
from tibian.tickets import Ticket


@pytest.fixture
def jira_mock(mocker):
    yield mocker.patch("tibian.sources.jira.JIRA", return_value=mocker.MagicMock())


@pytest.fixture
def jira_source_mock(jira_mock):
    yield JiraSource(
        "jira_name",
        {
            "url": "jira_url",
            "auth": {"username": "jira_username", "password": "jira_password"},
            "project": "jira_project",
        },
    )


class TestJiraSource:
    def test_correct_initialization(self, jira_source_mock, jira_mock):
        assert jira_source_mock.name == "jira_name"
        assert jira_source_mock.project == "jira_project"

        assert jira_source_mock.jira is not None
        jira_mock.assert_called_once_with("jira_url", auth=("jira_username", "jira_password"))

    def test_get_open_tickets(self, jira_source_mock):
        jira_issue_responses = [
            [
                Issue(
                    {},
                    None,
                    {
                        "key": "ABC-123",
                        "fields": {
                            "status": {"name": "Open"},
                            "summary": "ABC Ticket subscription",
                            "created": "2020-01-01",
                        },
                    },
                ),
                Issue(
                    {},
                    None,
                    {
                        "key": "ABC-456",
                        "fields": {
                            "status": {"name": "Closed"},
                            "summary": "ABC Ticket subscription",
                            "created": "2021-02-03",
                        },
                    },
                ),
            ],
            [
                Issue(
                    {},
                    None,
                    {
                        "key": "ABC-789",
                        "fields": {
                            "status": {"name": "Open"},
                            "summary": "ABC Ticket subscription",
                            "created": "2022-04-05",
                        },
                    },
                )
            ],
            [],
        ]

        jira_source_mock.jira.search_issues = mock.Mock(side_effect=jira_issue_responses)

        tickets = jira_source_mock.get_open_tickets()

        assert tickets == [
            Ticket("ABC-123", "ABC Ticket subscription", "Open", datetime.date(2020, 1, 1)),
            Ticket("ABC-789", "ABC Ticket subscription", "Open", datetime.date(2022, 4, 5)),
        ]
