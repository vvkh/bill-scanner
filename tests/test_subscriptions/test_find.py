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