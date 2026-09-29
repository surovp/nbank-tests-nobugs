from typing import Annotated

from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel


class CustomerProfileRequest(BaseModel):
    name: Annotated[str, GeneratingRule(regex=r'^[A-Za-z]+ [A-Za-z]+$')]
