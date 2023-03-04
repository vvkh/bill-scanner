import argparse
import typing

import scanner.transactions
import scanner.subcriptions


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', type=argparse.FileType('r'))
    parser.add_argument('--format', type=str, default=None)
    parser.add_argument('--ignore-pattern', type=str, default=None)
    return parser


def find_subscriptions(csv: typing.TextIO, format: str | None, ignore_pattern: str | None) -> list[str]:
    transactions = scanner.transactions.from_csv(csv, format=format)
    subscriptions = scanner.subcriptions.find(transactions, ignore_pattern=ignore_pattern)
    return [subscription.name for subscription in subscriptions]
