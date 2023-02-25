import os
import io
import datetime

import scanner.transactions

_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_CUR_DIR, 'data')


def test_from_csv():
    assert scanner.transactions.from_csv(io.StringIO('')) == []

    statement = open(os.path.join(_DATA_DIR, 'statement.csv'))
    transactions = scanner.transactions.from_csv(statement)
    assert transactions == [
        scanner.transactions.Transaction(
            amount=109.75,
            timestamp=datetime.datetime(year=2023, month=2, day=24),
            message='Payment - Amount: GEL109.75; Merchant: Wolt, Tbilisi, 61 Agmashenebeli ave. Tbilisi Georgia'
        ),
        scanner.transactions.Transaction(
            amount=10.00,
            timestamp=datetime.datetime(year=2023, month=2, day=25),
            message='Payment - Amount: GEL10.00; Merchant: Shukura, Georgia; MCC:5812; Date: 22/02/2023 00:00'
        ),
        scanner.transactions.Transaction(
            amount=5.99,
            timestamp=datetime.datetime(year=2023, month=2, day=26),
            message='Payment - Amount: USD5.99; Merchant: APPLE.COM/BILL, Ireland; MCC:5818; Date: 22/02/2023 00:00'
        ),
    ]
