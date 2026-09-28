from pydantic import BaseModel
from typing import List, Optional


class GetTransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int

class GetAccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[GetTransactionResponse]

class GetCustomerProfile(BaseModel):
    id: int
    username: str
    name: str | None
    role: str