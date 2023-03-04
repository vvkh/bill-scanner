import dataclasses
import datetime

from scanner.transactions import Transaction


@dataclasses.dataclass
class Subscription:
    name: str
    amount: float


def find(transactions: list[Transaction]) -> list[Subscription]:
    payments_by_title: dict[str, list[Transaction]] = {}
    for txn in transactions:
        if txn.message not in payments_by_title:
            payments_by_title[txn.message] = []
        payments_by_title[txn.message].append(txn)

    subscriptions = []
    for title, payments in payments_by_title.items():
        if len(payments) < 2:
            # we can't know if one-time payment is a subscription
            continue

        paid_amounts = set(txn.amount for txn in payments)
        if len(paid_amounts) > 1:
            # different amounts → probably not a subscription?
            # need to somehow support transactions in different currencies
            continue
        subscription_amount = paid_amounts.pop()

        time_periods_between_payments = [
            payment.timestamp - prev_payment.timestamp
            for prev_payment, payment in zip(payments[1:], payments)
        ]
        if max(time_periods_between_payments) <= _MAX_PERIOD_BETWEEN_PAYMENTS:
            subscriptions.append(
                Subscription(
                    name=title,
                    amount=subscription_amount,
                )
            )

    return subscriptions


# 1 month +/- 10 days
_MAX_PERIOD_BETWEEN_PAYMENTS = datetime.timedelta(days=40)


def _date_only(timestamp: datetime.datetime) -> tuple[int, int, int]:
    return timestamp.year, timestamp.month, timestamp.day

