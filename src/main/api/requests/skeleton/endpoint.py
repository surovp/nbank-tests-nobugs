from enum import Enum
from typing import List

from src.main.api.models.base_model import BaseModel
from dataclasses import dataclass

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.customer_profile_request import CustomerProfileRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.deposit_money_response import DepositMoneyResponse
from src.main.api.models.customer_profile_response import CustomerProfileResponse, CustomerResponse
from src.main.api.models.account_response import AccountsListResponse
from src.main.api.models.deposit_request_fraud import DepositRequestFraud
from src.main.api.models.deposit_response_fraud import DepositResponseFraud
from src.main.api.models.get_customer_profile import GetCustomerProfile
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.models.transfer_money_response_fraud import TransferResponseFraudCheck


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

    DEPOSIT_FRAUD = EndpointConfig(
        url='/accounts/deposit',
        request_model=DepositRequestFraud,
        response_model=DepositResponseFraud
    )

    EDIT_CUSTOMER_NAME = EndpointConfig(
        url='/customer/profile',
        request_model=CustomerProfileRequest,
        response_model=CustomerResponse
    )

    CUSTOMER_PROFILE = EndpointConfig(
        url='/customer/profile',
        request_model=None,
        response_model=GetCustomerProfile
    )

    ACCOUNTS = EndpointConfig(
        url='/customer/accounts',
        request_model=None,
        response_model=AccountsListResponse
    )

    ADMIN_GET_ALL_USERS = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=List[CreateUserResponse]
    )

    GET_CUSTOMER_ACCOUNTS = EndpointConfig(
        url='/customer/accounts',
        request_model=None,
        response_model=List[CreateAccountResponse]
    )

    TRANSFER_WITH_FRAUD_CHECK = EndpointConfig(
        url='/accounts/transfer-with-fraud-check',
        request_model=TransferMoneyRequest,
        response_model=TransferResponseFraudCheck
    )
