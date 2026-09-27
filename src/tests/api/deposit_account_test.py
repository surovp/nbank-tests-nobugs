from http import HTTPStatus

import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixtures import user_request
from src.main.api.generators.random_data import RandomData
from src.main.api.models.comparison.dao_and_model_assertions import DaoAndModelAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.specs.response_specs import DepositErrors


@pytest.mark.api
@pytest.mark.api_version("with_database_with_fix_with_swagger")
class TestDepositAccount:

    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.parametrize(
        argnames='balance',
        argvalues=[RandomData.get_deposit_amount(), 5000.00, 5000, 4999.99]
    )
    def test_deposit_account(self, user_request: CreateUserRequest, api_manager: ApiManager, balance):
        account = api_manager.user_steps.create_account(user_request)
        create = api_manager.deposit_steps.deposit(user_request, DepositMoneyRequest(
            accountId=account.id, amount=balance))

        dao_balance = api_manager.database_steps.get_account_by_account_number(create.accountNumber)
        DaoAndModelAssertions.assert_that(create, dao_balance).match()


    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.parametrize(
        argnames='balance, error_value',
        argvalues=[
            (0, DepositErrors.MIN_DEPOSIT_AMOUNT.value),
            (RandomData.negative_number(), DepositErrors.MIN_DEPOSIT_AMOUNT.value),
            (5000.01, DepositErrors.MAX_DEPOSIT_AMOUNT.value),
            (RandomData.get_invalid_deposit_amount(), DepositErrors.MAX_DEPOSIT_AMOUNT.value),
        ]
    )
    def test_invalid_balance_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            balance,
            error_value
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.invalid_deposit(
            user_request,
            DepositMoneyRequest(accountId=account.id, amount=balance),
            error_value
        )

        dao_balance = api_manager.database_steps.get_account_by_account_number(account.accountNumber)
        DaoAndModelAssertions.assert_that(account, dao_balance).match()

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    def test_invalid_id_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account: CreateAccountResponse
    ):
        api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.invalid_deposit(
            user_request,
            DepositMoneyRequest(accountId=user_with_account.id, amount=RandomData.get_deposit_amount()),
            DepositErrors.UNAUTHORIZED_ACCOUNT.value,
            HTTPStatus.FORBIDDEN
        )

        dao_balance = api_manager.database_steps.get_account_by_account_number(user_with_account.accountNumber)
        DaoAndModelAssertions.assert_that(user_with_account, dao_balance).match()

    @pytest.mark.usefixtures("api_manager", 'user_request')
    def test_not_found_account(self, api_manager: ApiManager, user_request: CreateUserRequest):
        acc_id = RandomData.get_invalid_account_id()
        api_manager.deposit_steps.invalid_deposit(
            user_request,
            DepositMoneyRequest(accountId=acc_id, amount=RandomData.get_deposit_amount()),
            DepositErrors.UNAUTHORIZED_ACCOUNT.value,
            HTTPStatus.FORBIDDEN
        )

        user_dao = api_manager.database_steps.find_account_by_account_id(acc_id)
        assert user_dao is None, f"User '{acc_id}' should NOT exist in DB after invalid create, but was found: {user_dao}"