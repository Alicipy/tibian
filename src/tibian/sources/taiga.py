from typing import Any, Literal, Union

import dateutil.parser
import requests
from pydantic import BaseModel, HttpUrl, SecretStr

from tibian.sources.ticketsource import TicketSource
from tibian.tickets import Ticket

TAIGA_API_PATH = "/api/v1"


class TaigaAuth(BaseModel):
    token: SecretStr


class TaigaSource(TicketSource):
    type: Literal["taiga"] = "taiga"
    url: HttpUrl
    project: int
    auth: TaigaAuth

    def get_open_tickets(self) -> list[Ticket]:
        open_issues = []
        search_url = self._get_taiga_search_url()
        content = self._request_issues(search_url)

        for story in content:
            ticket = self._extract_ticket_from_story(story)
            open_issues.append(ticket)

        return open_issues

    def _get_taiga_search_url(self) -> str:
        return f"{self.url}{TAIGA_API_PATH.strip('/')}/userstories"

    def _request_issues(self, search_url: str) -> list[dict[str, Any]]:
        query_params: dict[str, Union[float, str]] = {
            "project": self.project,
            "status__is_closed": "false",
        }
        headers = {
            "Authorization": f"Bearer {self.auth.token.get_secret_value()}",
            "x-disable-pagination": "True",
        }
        response = requests.get(
            search_url,
            params=query_params,
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()
        content: list[dict[str, Any]] = response.json()
        return content

    def _extract_ticket_from_story(self, story: dict[str, Any]) -> Ticket:
        key = str(story["ref"])
        title = story["subject"]
        status = story["status_extra_info"]["name"]
        created = dateutil.parser.parse(story["created_date"]).date()

        ticket = Ticket(key, title, status, created)
        return ticket
