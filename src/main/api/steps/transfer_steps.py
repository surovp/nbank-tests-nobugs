from typing import List

from src.main.api.models.account_response import AccountsListResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_step import BaseSteps
from src.main.api.utils.helpers import get_balance_account


class TransferSteps(BaseSteps):

    def transfer(self, user_request: CreateUserRequest, transfer_request: TransferMoneyRequest):

        balance_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        transfer_response: TransferMoneyResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_returns_ok()
        ).post(transfer_request)

        account_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        assert account_response[0].balance == balance_response[0].balance - transfer_request.amount
        assert transfer_response.message == "Transfer successful"

        return transfer_response

    def transfer_self_account(
            self,
            user_request: CreateUserRequest,
            transfer_request: TransferMoneyRequest
    ):
        balances_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        transfer_response: TransferMoneyResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_returns_ok()
        ).post(transfer_request)

        transfer_balances_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)


        assert get_balance_account(transfer_balances_response, transfer_request.senderAccountId) == \
               get_balance_account(balances_response, transfer_request.senderAccountId) - transfer_request.amount

        assert get_balance_account(transfer_balances_response, transfer_request.receiverAccountId) == \
               get_balance_account(balances_response, transfer_request.receiverAccountId) + transfer_request.amount

        return transfer_response

    def invalid_transfer(
            self,
            user_request: CreateUserRequest,
            transfer_request: TransferMoneyRequest,
            error_value: str,
            error_key: None = None,
    ):
        balance_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_returns_bad_request(error_value, error_key)
        ).post(transfer_request)

        account_response: List[AccountsListResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get(as_list=True)

        assert account_response[0].balance == balance_response[0].balance