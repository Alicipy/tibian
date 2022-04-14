import json
from typing import TYPE_CHECKING, List

import requests

if TYPE_CHECKING:
    from tibian.tickets import BirthdayTicket

import tibian.vars
from tibian.targets.target import Target


class TeamsTarget(Target):

    TYPENAME = "teams"

    def __init__(self, name: str, config: dict, *args, **kwargs) -> None:
        super().__init__(name, config, *args, **kwargs)
        self.url = config["url"]

    def announce_birthdays(self, birthday_tickets: List["BirthdayTicket"]) -> None:

        base_content = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Birthdays",
            "sections": [
                {
                    "activityTitle": f"{tibian.vars.get_today()}",
                    "facts": [],
                    "text": "",
                    "markdown": True,
                }
            ],
        }

        body = base_content["sections"][0]
        assert isinstance(body, dict)

        if birthday_tickets:
            body["facts"] = [
                {"name": ticket.name, "value": f"{ticket.title} ({ticket.age} year(s))"}
                for ticket in birthday_tickets
            ]
        else:
            body["text"] = "**It's no tickets birthday today :(**"

        headers = {"Content-Type": "application/json"}

        res = requests.post(self.url, data=json.dumps(base_content), headers=headers, timeout=10)

        res.raise_for_status()
