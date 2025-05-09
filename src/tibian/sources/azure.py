from itertools import islice
from typing import Literal

import dateutil.parser
import requests
from pydantic import BaseModel, SecretStr

from tibian.sources.ticketsource import TicketSource
from tibian.tickets import Ticket

AZURE_API_VERSION = "7.0"
MAX_TICKETS_PER_REQUEST = 100

OPEN_TICKETS_WIQL_QUERY = {
    "query": """
     SELECT *
     FROM workitems
     WHERE [System.WorkItemType] IN ('User Story', 'Bug')
       AND [System.State] <> 'Resolved'
       AND [System.State] <> 'Closed'
       AND [System.State] <> 'Removed'
     ORDER BY [System.ChangedDate] DESC
     """
}


class AzureAuth(BaseModel):
    token: SecretStr


class AzureSource(TicketSource):
    type: Literal["azure"] = "azure"
    organization: str
    project: str
    auth: AzureAuth

    def get_open_tickets(self) -> list[Ticket]:
        ticket_ids = self._get_open_tickets_ids()
        ticket_details = self._get_ticket_details(ticket_ids)
        return ticket_details

    def _get_open_tickets_ids(self) -> list[str]:
        open_tickets_url = f"{self._get_azure_api_url()}/wit/wiql?api-version={AZURE_API_VERSION}"
        response = requests.post(
            open_tickets_url,
            auth=("", self.auth.token.get_secret_value()),
            headers={"Content-Type": "application/json"},
            json=OPEN_TICKETS_WIQL_QUERY,
            timeout=3,
        )
        response.raise_for_status()
        content = response.json()
        ids = [str(work_item["id"]) for work_item in content["workItems"]]
        return ids

    def _get_ticket_details(self, ticket_ids: list[str]) -> list[Ticket]:
        workitemsbatch_url = (
            f"{self._get_azure_api_url()}/wit/workitemsbatch?api-version={AZURE_API_VERSION}"
        )

        ticket_ids_iter = iter(ticket_ids)
        results: list[Ticket] = []
        while True:
            chunk = list(islice(ticket_ids_iter, MAX_TICKETS_PER_REQUEST))
            if not chunk:
                break

            ticket_details_query = {
                "ids": chunk,
                "fields": [
                    "System.Title",
                    "System.State",
                    "System.CreatedDate",
                ],
            }

            response = requests.post(
                workitemsbatch_url,
                json=ticket_details_query,
                auth=("", self.auth.token.get_secret_value()),
                headers={"Content-Type": "application/json"},
                timeout=3,
            )
            response.raise_for_status()
            content = response.json().get("value", [])

            for work_item in content:
                ticket_id = str(work_item["id"])
                ticket_fields = work_item["fields"]

                results.append(
                    Ticket(
                        ticket_id,
                        ticket_fields["System.Title"],
                        ticket_fields["System.State"],
                        dateutil.parser.parse(ticket_fields["System.CreatedDate"]).date(),
                    )
                )

        return results

    def _get_azure_api_url(self) -> str:
        return f"https://dev.azure.com/{self.organization}/{self.project}/_apis"
