import argparse
import typing

import scanner.transactions
import scanner.subcriptions


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', type=argparse.FileType('r'))
    return parser


def find_subscriptions(csv: typing.TextIO) -> list[str]:
    transactions = scanner.transactions.from_csv(csv)
    subscriptions = scanner.subcriptions.find(transactions)
    return [subscription.name for subscription in subscriptions]
