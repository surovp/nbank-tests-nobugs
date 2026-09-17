from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TransactionsDao:
    """
    Representation of a row in 'transactions' table.
    Field names are expected to match DB columns (snake_case).
    """

    id: int
    amount: float
    type: str
    timestamp: datetime
    account_id: int
    related_account_id: int
    created_at: datetime
