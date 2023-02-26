import argparse
import typing

import scanner.transactions
import scanner.subcriptions


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', type=argparse.FileType('r'))
    parser.add_argument('--format', type=str, default=None)
    return parser


def find_subscriptions(csv: typing.TextIO, format: str | None) -> list[str]:
    transactions = scanner.transactions.from_csv(csv, format=format)
    subscriptions = scanner.subcriptions.find(transactions)
    return [subscription.name for subscription in subscriptions]
