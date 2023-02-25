import dataclasses
import datetime


@dataclasses.dataclass
class Transaction:
    message: str
    timestamp: datetime.datetime
    amount: int
