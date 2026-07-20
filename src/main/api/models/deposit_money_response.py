from src.main.api.models.base_model import BaseModel
from typing import List


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int

class DepositMoneyResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[TransactionResponse]
