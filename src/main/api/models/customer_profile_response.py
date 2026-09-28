from pydantic import BaseModel
from typing import List, Optional

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int

class AccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: Optional[List[TransactionResponse]] = []

class CustomerResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str

class CustomerProfileResponse(BaseModel):
    customer: CustomerResponse
    message: str