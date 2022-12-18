import datetime


import subscriptions


def test_find():
    transactions = [
        subscriptions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
    ]

    assert subscriptions.find(transactions) == []


    transactions = [
        subscriptions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        subscriptions.Transaction(
            message="Lunch",
            timestamp=datetime.datetime.fromisoformat("2020-02-01T00:00:00"),
            amount=200
        ),
    ]
    assert subscriptions.find(transactions) == []

    transactions = [
        subscriptions.Transaction(
            message="Coffee",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        subscriptions.Transaction(
            message="Lunch",
            timestamp=datetime.datetime.fromisoformat("2020-02-02T00:00:00"),
            amount=100
        ),
    ]
    assert subscriptions.find(transactions) == []

    transactions = [
        subscriptions.Transaction(
            message="Netflix",
            timestamp=datetime.datetime.fromisoformat("2020-01-01T00:00:00"),
            amount=100
        ),
        subscriptions.Transaction(
            message="Netflix",
            timestamp=datetime.datetime.fromisoformat("2020-02-01T00:00:00"),
            amount=100
        ),
    ]
    assert subscriptions.find(transactions) == [
        subscriptions.Subscription(
            name="Netflix",
            amount=100,
        )
    ]