import math
from typing import List

from src.main.api.models.account_response import AccountsListResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.deposit_money_response import DepositMoneyResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_step import BaseSteps
from src.main.api.utils.helpers import max_deposit_value, get_balance_account


class DepositSteps(BaseSteps):

    def deposit(self, user_request: CreateUserRequest, deposit_request: DepositMoneyRequest):
        deposit_response: DepositMoneyResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_returns_ok()
        ).post(deposit_request)

        balances_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        assert deposit_response.balance == deposit_request.balance
        assert get_balance_account(balances_response, deposit_request.id) == deposit_request.balance
        assert deposit_response.transactions

        return deposit_response

    def deposit_any_amount(self, user_request: CreateUserRequest, account_id: int, sum_iter: int | float):
        iterations = math.ceil(sum_iter / max_deposit_value())

        deposit_request = DepositMoneyRequest(id=account_id, balance=max_deposit_value())

        for _ in range(iterations):
            deposit_response: DepositMoneyResponse = ValidatedCrudRequester(
                RequestSpecs.auth_as_user(user_request.username, user_request.password),
                Endpoint.DEPOSIT_MONEY,
                ResponseSpecs.request_returns_ok()
            ).post(deposit_request)

            assert deposit_response.transactions


    def invalid_deposit(
            self,
            user_request: CreateUserRequest,
            deposit_request: DepositMoneyRequest,
            error_value: str,
            expected_status: int = 400,
            error_key: None = None
    ):
        spec_factories = {
            400: ResponseSpecs.request_returns_bad_request,
            403: ResponseSpecs.request_returns_forbidden,
        }
        if expected_status not in spec_factories:
            raise ValueError(
                f"Unsupported status code: {expected_status}. "
                f"Supported: {list(spec_factories.keys())}"
            )

        CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.DEPOSIT_MONEY,
            spec_factories[expected_status](error_value, error_key)
        ).post(deposit_request)

        balances_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        assert get_balance_account(balances_response, deposit_request.id) == 0