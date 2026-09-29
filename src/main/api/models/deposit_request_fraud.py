from src.main.api.models.base_model import BaseModel


class DepositRequestFraud(BaseModel):
    accountId: int
    amount: float
