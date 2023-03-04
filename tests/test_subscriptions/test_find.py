import datetime


import scanner
import scanner.subcriptions
import scanner.transactions


def test_find():
    transactions = [
        scanner.transactions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
    ]

    assert scanner.subcriptions.find(transactions) == []


    transactions = [
        scanner.transactions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        scanner.transactions.Transaction(
            message="Lunch",
            timestamp=datetime.datetime.fromisoformat("2020-02-01T00:00:00"),
            amount=200
        ),
    ]
    assert scanner.subcriptions.find(transactions) == []

    transactions = [
        scanner.transactions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        scanner.transactions.Transaction(
            message="Lunch",
            timestamp=datetime.datetime.fromisoformat("2020-02-02T00:00:00"),
            amount=100
        ),
    ]
    assert scanner.subcriptions.find(transactions) == []

    transactions = [
        scanner.transactions.Transaction(
            message="Netflix",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        scanner.transactions.Transaction(
            message="Netflix",
            timestamp=datetime.datetime.fromisoformat("2020-02-01T00:00:00"),
            amount=100
        ),
    ]
    assert scanner.subcriptions.find(transactions) == [
        scanner.subcriptions.Subscription(
            name="Netflix",
            amount=100,
        )
    ]


def test_find_variable_period():
    """
    Sometimes subscription payments are not made on the same day of the month.
    """
    transactions = [
        scanner.transactions.Transaction(
            message="EXPRESSVPN.COM",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=2, day=22),
        ),
        scanner.transactions.Transaction(
            message="EXPRESSVPN.COM",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=1, day=21),
        ),
        scanner.transactions.Transaction(
            message="EXPRESSVPN.COM",
            amount=12.95,
            timestamp=datetime.datetime(year=2022, month=12, day=23),
        )
    ]
    assert scanner.subcriptions.find(transactions) == [
        scanner.subcriptions.Subscription(
            name="EXPRESSVPN.COM",
            amount=12.95,
        ),
    ]

    reverse_order = list(reversed(transactions))
    assert scanner.subcriptions.find(reverse_order) == [
        scanner.subcriptions.Subscription(
            name="EXPRESSVPN.COM",
            amount=12.95,
        ),
    ]


def test_find_exceeding_variable_period_limit():
    transactions = [
        scanner.transactions.Transaction(
            message="EXPRESSVPN.COM",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=3, day=22),
        ),
        scanner.transactions.Transaction(
            message="EXPRESSVPN.COM",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=1, day=22),
        ),
    ]
    assert scanner.subcriptions.find(transactions) == []

    reverse_order = list(reversed(transactions))
    assert scanner.subcriptions.find(reverse_order) == []



def test_find_variable_message():
    """
    Sometimes message is different for the same subscription.
    For example, they can include the date of the payment.
    """
    transactions = [
        scanner.transactions.Transaction(
            message="Payment - Amount: USD12.95; Merchant: EXPRESSVPN.COM, Cyprus; Date: 22/02/2023 23:50",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=2, day=22),
        ),
        scanner.transactions.Transaction(
            message="Payment - Amount: USD12.95; Merchant: EXPRESSVPN.COM, Cyprus; Date: 21/01/2023 23:50",
            amount=12.95,
            timestamp=datetime.datetime(year=2023, month=1, day=21),
        ),
        scanner.transactions.Transaction(
            message="Payment - Amount: USD12.95; Merchant: EXPRESSVPN.COM, Cyprus; Date: 23/12/2022 23:50",
            amount=12.95,
            timestamp=datetime.datetime(year=2022, month=12, day=23),
        )
    ]
    assert scanner.subcriptions.find(transactions, ignore_pattern=r'Date: \d\d/\d\d/\d\d\d\d \d\d:\d\d') == [
        scanner.subcriptions.Subscription(
            name="Payment - Amount: USD12.95; Merchant: EXPRESSVPN.COM, Cyprus; ",
            amount=12.95,
        ),
    ]

