import dataclasses
import datetime
import typing
import csv

import scanner.errors


@dataclasses.dataclass
class Transaction:
    message: str
    timestamp: datetime.datetime
    amount: float


def from_csv(transactions_csv: typing.TextIO, format: str | None = None) -> list[Transaction]:
    reader = csv.reader(transactions_csv, delimiter=',', quotechar='"')
    timestamp_parser, message_parser, amount_parser = _parse_format(format)

    try:
        next(reader)  # skip header
    except StopIteration:
        return []

    result = []
    for row in reader:
        result.append(Transaction(
            message=message_parser(row),
            timestamp=timestamp_parser(row),
            amount=amount_parser(row),
        ))
    return sorted(result, key=lambda txn: txn.timestamp)


_DEFAULT_FORMAT = 'timestamp,message,amount'
_AMOUNT_PARSER = typing.Callable[[list[str]], float]
_TIMESTAMP_PARSER = typing.Callable[[list[str]], datetime.datetime]
_MESSAGE_PARSER = typing.Callable[[list[str]], str]


def _parse_format(format: str | None) -> tuple[_TIMESTAMP_PARSER, _MESSAGE_PARSER, _AMOUNT_PARSER]:
    format = format or _DEFAULT_FORMAT
    fields = format.split(',')

    try:
        message_field = fields.index('message')
    except ValueError:
        raise scanner.errors.BadFormat('Missing message field. Required fields: timestamp, message, amount')

    try:
        timestamp_field = fields.index('timestamp')
    except ValueError:
        raise scanner.errors.BadFormat('Missing timestamp field. Required fields: timestamp, message, amount')

    amount_fields = [i for i, label in enumerate(fields) if label == 'amount']
    if not amount_fields:
        raise scanner.errors.BadFormat('Missing amount field. Required fields: timestamp, message, amount')

    def parse_timestamp(row: list[str]) -> datetime.datetime:
        return datetime.datetime.strptime(row[timestamp_field], '%d.%m.%Y')

    def parse_message(row: list[str]) -> str:
        return row[message_field]

    def parse_amount(row: list[str]) -> float:
        for i in amount_fields:
            try:
                amount = float(row[i])
            except ValueError:
                continue

            if amount < 0:
                amount = -amount
            return amount
        raise scanner.errors.BadCSV(f'No amount found in field(s) {amount_fields}. Did you specify format correctly?')

    return parse_timestamp, parse_message, parse_amount
