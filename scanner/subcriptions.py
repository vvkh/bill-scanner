import dataclasses
import datetime
import re

from scanner.transactions import Transaction


@dataclasses.dataclass
class Subscription:
    name: str
    amount: float


def find(transactions: list[Transaction], ignore_pattern: str | None = None) -> list[Subscription]:
    payments_by_title: dict[str, list[Transaction]] = {}
    for txn in transactions:
        title = txn.message
        if ignore_pattern:
            title = re.sub(ignore_pattern, '', title)
        if title not in payments_by_title:
            payments_by_title[title] = []
        payments_by_title[title].append(txn)

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
