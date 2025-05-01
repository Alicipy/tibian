from typing import List, Any, Literal

import dateutil.parser
from pydantic import BaseModel, HttpUrl
import requests

from tibian.sources.ticketsource import TicketSource
from tibian.tickets import Ticket

JIRA_API_PATH = "/rest/api/3"


class JiraAuth(BaseModel):
    username: str
    password: str


class JiraSource(TicketSource):
    type: Literal["jira"] = "jira"
    url: HttpUrl
    project: str
    auth: JiraAuth

    def get_open_tickets(self) -> List[Ticket]:
        open_issues = []
        search_url = self._get_jira_search_url()
        query_params = {
            "jql": self._build_jql_query(),
            "fields": "summary,status,created",
            "properties": "",
        }

        while True:
            response = requests.get(
                search_url,
                params=query_params,
                auth=(self.auth.username, self.auth.password),
                timeout=5,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            content = response.json()

            for issue in content["issues"]:
                ticket = self._extract_ticket_from_issue(issue)
                open_issues.append(ticket)

            if not (nextPageToken := content.get("nextPageToken")):
                break

            query_params["nextPageToken"] = nextPageToken

        return open_issues

    def _get_jira_search_url(self) -> str:
        return f"{self.url}{JIRA_API_PATH.strip('/')}/search/jql"

    def _extract_ticket_from_issue(self, issue: dict[str, Any]) -> Ticket:
        fields = issue["fields"]
        key = issue["key"]
        title = fields["summary"]
        status = fields["status"]["name"]
        created = dateutil.parser.parse(fields["created"]).date()
        ticket = Ticket(key, title, status, created)
        return ticket

    def _build_jql_query(self) -> str:
        return f"project = {self.project} AND status not in (Done, Cancelled, Closed) AND issuetype in standardIssueTypes() AND issuetype not in (Epic, Sub-task)"
