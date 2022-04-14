from tibian.config import construct_objects_based_on_config_type, load_config
from tibian.tickets import (
    announce_birthdays,
    collect_open_tickets,
    filter_for_birthday_tickets,
)


def main():

    config = load_config()

    sources = construct_objects_based_on_config_type(config["sources"])
    targets = construct_objects_based_on_config_type(config["destinations"])

    open_tickets = collect_open_tickets(sources)
    birthday_tickets = filter_for_birthday_tickets(open_tickets)

    announce_birthdays(targets, birthday_tickets)


if __name__ == "__main__":
    main()
