import datetime

from tibian.main import main
from tibian.tickets import BirthdayTicket, Ticket


def test_main(mocker):

    mocker.patch("tibian.vars.get_today", return_value=datetime.date(2022, 3, 1))

    mocker.patch("tibian.main.load_config", return_value={"sources": [], "destinations": []})
    mocker.patch(
        "tibian.main.collect_open_tickets",
        return_value=[
            Ticket("A", "ABC Ticket subscription", "open", datetime.date(2021, 3, 1)),
            Ticket("B", "ABC Ticket subscription", "open", datetime.date(2001, 1, 1)),
        ],
    )
    announce_mock = mocker.patch("tibian.main.announce_birthdays", return_value=None)

    main()

    announce_mock.assert_called_once_with(
        [], [BirthdayTicket("A", "ABC Ticket subscription", "open", datetime.date(2021, 3, 1))]
    )
