from pydantic import BaseModel
from typing import List, Optional


class GetTransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int


class AccountsListResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: Optional[List[GetTransactionResponse]] = []
