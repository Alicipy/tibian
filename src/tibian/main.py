from tibian.config import load_config
from tibian.tickets import (
    announce_birthdays,
    collect_open_tickets,
    filter_for_birthday_tickets,
)


def main() -> None:
    tibian_config = load_config()

    open_tickets = collect_open_tickets(tibian_config.sources)
    birthday_tickets = filter_for_birthday_tickets(open_tickets)

    announce_birthdays(tibian_config.destinations, birthday_tickets)


if __name__ == "__main__":
    main()
