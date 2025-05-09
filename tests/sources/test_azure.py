import datetime

import pytest
from pydantic import SecretStr

from tibian.sources.azure import AzureAuth, AzureSource
from tibian.tickets import Ticket


@pytest.fixture
def azure_source():
    return AzureSource(
        name="azure-source",
        organization="test-org",
        project="test-project",
        auth=AzureAuth(token=SecretStr("mock_token")),
    )


def test_get_open_tickets(azure_source, requests_mock):
    open_work_items_response = [
        {
            "id": 123,
            "url": "https://dev.azure.com/test-org/test-project/_apis/wit/workitems/123",
        },
        {
            "id": 456,
            "url": "https://dev.azure.com/test-org/test-project/_apis/wit/workitems/456",
        },
    ]
    open_work_items_details = [
        {
            "id": 123,
            "fields": {
                "System.Title": "Fix login issue",
                "System.State": "In Progress",
                "System.CreatedDate": "2023-01-05T07:54:22Z",
            },
        },
        {
            "id": 456,
            "fields": {
                "System.Title": "Add new feature",
                "System.State": "New",
                "System.CreatedDate": "2023-03-18T16:12:34Z",
            },
        },
    ]

    requests_mock.post(
        "https://dev.azure.com/test-org/test-project/_apis/wit/wiql?api-version=7.0",
        json={"workItems": open_work_items_response},
    )
    requests_mock.post(
        "https://dev.azure.com/test-org/test-project/_apis/wit/workitemsbatch?api-version=7.0",
        json={"value": open_work_items_details},
    )

    tickets = azure_source.get_open_tickets()
    assert len(requests_mock.request_history) == 2
    last_request = requests_mock.last_request

    assert last_request.headers["Authorization"] == "Basic Om1vY2tfdG9rZW4="

    assert tickets == [
        Ticket(
            name="123",
            title="Fix login issue",
            status="In Progress",
            creation_date=datetime.date(2023, 1, 5),
        ),
        Ticket(
            name="456",
            title="Add new feature",
            status="New",
            creation_date=datetime.date(2023, 3, 18),
        ),
    ]
