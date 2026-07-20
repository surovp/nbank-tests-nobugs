import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.transfer_money_request import TransferMoneyRequest


@pytest.mark.api
class TestTransferMoney:

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='balance, amount, use_self_account',
        argvalues=[
            (5000, 0.01, True),
            (10000.00, 9999.99, True),
            (10000.00, 10000.00, True),
            (10000.00, RandomData.get_deposit_amount(), True),
            (5000, 5000, True),
            (5000, 4999.99, True),
            (15000, 10000, True),
            (5000, 0.01, False),
            (10000.00, 9999.99, False),
            (10000.00, 10000.00, False),
            (10000.00, RandomData.get_deposit_amount(), False),
            (5000, 5000, False),
            (5000, 4999.99, False),
            (15000, 10000, False)
        ]
    )
    def test_transfer_amount(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            use_self_account,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_more_5000(user_request, account.id, balance)

        if use_self_account:
            api_manager.transfer_steps.transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=account.id, amount=amount)
            )
        else:
            api_manager.transfer_steps.transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=amount)
            )

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='balance, amount, error_value, use_self_account',
        argvalues=[
            (10000, 10000.01, 'Transfer amount cannot exceed 10000', True),
            (10000, 0, 'Transfer amount must be at least 0.01', True),
            (10000, RandomData.negative_number(), 'Transfer amount must be at least 0.01', True),
            (RandomData.get_deposit_amount(), 10000, 'Invalid transfer: insufficient funds or invalid accounts', True),
            (10000, 10000.01, 'Transfer amount cannot exceed 10000', False),
            (10000, 0, 'Transfer amount must be at least 0.01', False),
            (10000, RandomData.negative_number(), 'Transfer amount must be at least 0.01', False),
            (RandomData.get_deposit_amount(), 10000, 'Invalid transfer: insufficient funds or invalid accounts', False),
        ]
    )
    def test_transfer_invalid_amount(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            use_self_account,
            error_value,
            balance,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)
        api_manager.deposit_steps.deposit_more_5000(user_request, account.id, balance)

        if use_self_account:
            api_manager.transfer_steps.invalid_transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=account.id, amount=amount),
                error_value
            )
        else:
            api_manager.transfer_steps.invalid_transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=amount),
                error_value
            )

    @pytest.mark.usefixtures("api_manager", 'user_request', 'user_with_account')
    @pytest.mark.parametrize(
        argnames='amount, error_value, use_self_account',
        argvalues=[
            (RandomData.get_deposit_amount(), 'Invalid transfer: insufficient funds or invalid accounts', True),
            (RandomData.get_deposit_amount(), 'Invalid transfer: insufficient funds or invalid accounts', False),
        ]
    )
    def test_transfer_empty_balance(
            self,
            user_request: CreateUserRequest,
            api_manager: ApiManager,
            user_with_account,
            use_self_account,
            error_value,
            amount
    ):
        account = api_manager.user_steps.create_account(user_request)

        if use_self_account:
            api_manager.transfer_steps.invalid_transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=account.id, amount=amount),
                error_value
            )
        else:
            api_manager.transfer_steps.invalid_transfer(
                user_request,
                TransferMoneyRequest(senderAccountId=account.id, receiverAccountId=user_with_account.id, amount=amount),
                error_value
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
            'Invalid transfer: insufficient funds or invalid accounts'
        )
