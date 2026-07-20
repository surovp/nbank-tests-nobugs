from enum import Enum

from src.main.api.models.base_model import BaseModel
from dataclasses import dataclass

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.customer_profile_request import CustomerProfileRequest
from src.main.api.models.customer_profile_response import CustomerProfileResponse
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.deposit_money_response import DepositMoneyResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model:BaseModel
    response_model:BaseModel

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url = '/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfig(
        url='/auth/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model=None,
        response_model=CreateAccountResponse
    )

    TRANSFER_MONEY = EndpointConfig(
        url='/accounts/transfer',
        request_model=TransferMoneyRequest,
        response_model=TransferMoneyResponse
    )

    DEPOSIT_MONEY = EndpointConfig(
        url='/accounts/deposit',
        request_model=DepositMoneyRequest,
        response_model=DepositMoneyResponse
    )

    CUSTOMER_NAME = EndpointConfig(
        url='/customer/profile',
        request_model=CustomerProfileRequest,
        response_model=CustomerProfileResponse
    )

