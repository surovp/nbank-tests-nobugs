from typing import Annotated

from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel


class DepositMoneyRequest(BaseModel):
    id: int
    balance: Annotated[float,GeneratingRule(
        regex=r'^(?:[1-9][0-9]{0,3}(?:\.[0-9]{1,2})?|5000(?:\.00)?|0\.[1-9][0-9]?|0\.[0-9][1-9])$')
    ]