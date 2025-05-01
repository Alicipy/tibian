from typing import List, Any

import dateutil.parser
import requests

from tibian.sources.ticketsource import TicketSource
from tibian.tickets import Ticket

JIRA_API_PATH = "/rest/api/3"


class JiraSource(TicketSource):
    TYPENAME = "jira"

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        super().__init__(name, config)

        url = config["url"]
        auth = config["auth"]

        self._username, self._password = auth["username"], auth["password"]

        self._issue_search_url = f"{url}{JIRA_API_PATH}/search/jql"
        self._project = config["project"]

    def get_open_tickets(self) -> List[Ticket]:
        open_issues = []
        query_params = {
            "jql": self._build_jql_query(),
            "fields": "summary,status,created",
            "properties": "",
        }
        while True:
            response = requests.get(
                self._issue_search_url,
                params=query_params,
                auth=(self._username, self._password),
                timeout=1,
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

    def _extract_ticket_from_issue(self, issue: dict[str, Any]) -> Ticket:
        fields = issue["fields"]
        key = issue["key"]
        title = fields["summary"]
        status = fields["status"]["name"]
        created = dateutil.parser.parse(fields["created"]).date()
        ticket = Ticket(key, title, status, created)
        return ticket

    def _build_jql_query(self) -> str:
        return f"project = {self._project} AND \
                status not in (Done, Cancelled, Closed) AND \
                issuetype in standardIssueTypes() AND \
                issuetype not in (Epic, Sub-task)"
