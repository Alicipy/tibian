from typing import List

import dateutil.parser
from jira import JIRA
from jira.client import Issue

from tibian.sources.ticketsource import TicketSource
from tibian.tickets import Ticket


class JiraSource(TicketSource):

    TYPENAME = "jira"

    def __init__(self, name: str, config: dict, *args, **kwargs) -> None:
        super().__init__(name, config)

        url = config["url"]
        auth = config["auth"]
        username, password = auth["username"], auth["password"]

        self.jira = JIRA(url, auth=(username, password))
        self.project = config["project"]

    def get_open_tickets(self) -> List[Ticket]:

        block_size = 250
        block_num = 0
        open_issues = []
        while True:
            start_index = block_num * block_size
            issues = self.jira.search_issues(f"project = {self.project}", start_index, block_size)
            if not issues:
                break
            block_num += 1

            for issue in issues:
                assert isinstance(issue, Issue)
                if issue.fields.status.name not in ["Closed", "Cancelled", "Done"]:
                    open_issues.append(
                        Ticket(
                            name=issue.key,
                            title=issue.fields.summary,
                            status=issue.fields.status.name,
                            creation_date=dateutil.parser.parse(issue.fields.created).date(),
                        )
                    )

        return open_issues
