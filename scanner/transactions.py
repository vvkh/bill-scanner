import dataclasses
import datetime
import typing
import csv


@dataclasses.dataclass
class Transaction:
    message: str
    timestamp: datetime.datetime
    amount: float


def from_csv(transactions_csv: typing.TextIO) -> list[Transaction]:
    reader = csv.reader(transactions_csv, delimiter=',', quotechar='"')
    try:
        next(reader)  # skip header
    except StopIteration:
        return []

    result = []
    for row in reader:
        amount = float(row[2])
        if amount < 0:
            amount = -amount
        timestamp = datetime.datetime.strptime(row[0], '%d.%m.%Y')
        result.append(Transaction(
            message=row[1],
            timestamp=timestamp,
            amount=amount,
        ))
    return sorted(result, key=lambda txn: txn.timestamp)
