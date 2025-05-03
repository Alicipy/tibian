import datetime

import pytest
from pydantic import HttpUrl, SecretStr

from tibian.sources.taiga import TaigaAuth, TaigaSource
from tibian.tickets import Ticket


@pytest.fixture
def taiga_source():
    return TaigaSource(
        name="taiga-source",
        url=HttpUrl("https://taiga.example.com"),
        project=42,
        auth=TaigaAuth(token=SecretStr("mock_token")),
    )


def test_get_open_tickets(taiga_source, requests_mock):
    mock_stories = [
        {
            "ref": 101,
            "subject": "Fix login issue",
            "status_extra_info": {"name": "In Progress"},
            "created_date": "2023-01-05T07:54:22Z",
        },
        {
            "ref": 102,
            "subject": "Add new feature",
            "status_extra_info": {"name": "Open"},
            "created_date": "2023-03-18T16:12:34Z",
        },
    ]

    requests_mock.get("https://taiga.example.com/api/v1/userstories", json=mock_stories)

    tickets = taiga_source.get_open_tickets()
    assert len(requests_mock.request_history) == 1
    last_request = requests_mock.last_request

    assert last_request.headers["Authorization"] == "Bearer mock_token"
    assert last_request.qs == {"project": ["42"], "status__is_closed": ["false"]}

    assert tickets == [
        Ticket(
            name="101",
            title="Fix login issue",
            status="In Progress",
            creation_date=datetime.date(2023, 1, 5),
        ),
        Ticket(
            name="102",
            title="Add new feature",
            status="Open",
            creation_date=datetime.date(2023, 3, 18),
        ),
    ]
