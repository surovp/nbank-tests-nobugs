import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.specs.response_specs import TransferErrors


@pytest.mark.api
class TestTransferMoney:

    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.parametrize(
        argnames='balance, amount',
        argvalues=[
            (5000, 0.01),
            (10000.00, 9999.99),
            (10000.00, 10000.00),
            (10000.00, RandomData.get_deposit_amount()),
            (5000, 5000),
            (5000, 4999.99),
            (15000, 10000)
        ]
    )
    def test_transfer_amount_self(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        second_account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_any_amount(user_request, account.id, balance)
        api_manager.transfer_steps.transfer_self_account(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=second_account.id, amount=amount)
        )

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='balance, amount',
        argvalues=[
            (5000, 0.01),
            (10000.00, 9999.99),
            (10000.00, 10000.00),
            (10000.00, RandomData.get_deposit_amount()),
            (5000, 5000),
            (5000, 4999.99),
            (15000, 10000)
        ]
    )
    def test_transfer_amount_another_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_any_amount(user_request, account.id, balance)
        api_manager.transfer_steps.transfer(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=amount)
        )

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='balance, amount, error_value',
        argvalues=[
            (10000, 10000.01, TransferErrors.MAX_TRANSFER_AMOUNT.value),
            (10000, 0, TransferErrors.MIN_TRANSFER_AMOUNT.value),
            (10000, RandomData.negative_number(), TransferErrors.MIN_TRANSFER_AMOUNT.value),
            (RandomData.get_deposit_amount(), 10000, TransferErrors.INVALID_TRANSFER.value)
        ]
    )
    def test_transfer_invalid_amount_self(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            error_value,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_any_amount(user_request, account.id, balance)
        api_manager.transfer_steps.invalid_transfer(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=account.id, amount=amount),
            error_value
        )


    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='balance, amount, error_value',
        argvalues=[
            (10000, 10000.01, TransferErrors.MAX_TRANSFER_AMOUNT.value),
            (10000, 0, TransferErrors.MIN_TRANSFER_AMOUNT.value),
            (10000, RandomData.negative_number(), TransferErrors.MIN_TRANSFER_AMOUNT.value),
            (RandomData.get_deposit_amount(), 10000, TransferErrors.INVALID_TRANSFER.value),
        ]
    )
    def test_transfer_invalid_amount_another_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            error_value,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_any_amount(user_request, account.id, balance)
        api_manager.transfer_steps.invalid_transfer(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=amount),
            error_value
        )

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    def test_transfer_empty_balance_self(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.transfer_steps.invalid_transfer(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=account.id, amount=RandomData.get_deposit_amount()),
            TransferErrors.INVALID_TRANSFER.value
        )


    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    def test_transfer_empty_balance_another_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.transfer_steps.invalid_transfer(
            user_request,
            TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=RandomData.get_deposit_amount()),
            TransferErrors.INVALID_TRANSFER.value
        )

    @pytest.mark.usefixtures("api_manager", 'user_request')
    def test_transfer_invalid_account(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager
    ):
        account = api_manager.user_steps.create_account(user_request)
        balance = RandomData.get_deposit_amount()
        api_manager.deposit_steps.deposit(user_request, DepositMoneyRequest(id=account.id, balance=balance))
        api_manager.transfer_steps.invalid_transfer(
            user_request,
            TransferMoneyRequest(
                senderAccountId=account.id,
                receiverAccountId=RandomData.get_invalid_account_id(),
                amount=balance//2
            ),
            TransferErrors.INVALID_TRANSFER.value
        )
