import pytest
from playwright.sync_api import expect, Page
from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.customer_profile_request import CustomerProfileRequest
from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.utils.helpers import max_deposit_value, get_balance_account
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.transfer_page import TransferMoney


@pytest.mark.ui
class TestTransferMoney:
    @pytest.mark.user_session(1)
    @pytest.mark.browsers('chromium')
    def test_user_can_transfer_money_self(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        acc1 = api_manager.user_steps.create_account(user_request)
        acc2 = api_manager.user_steps.create_account(user_request)
        amount = RandomData.get_deposit_amount()
        api_manager.deposit_steps.deposit(user_request, DepositMoneyRequest(id=acc1.id, balance=max_deposit_value()))

        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money(
            account=acc1.id,
            recipient_account=acc2.accountNumber,
            amount=amount,
            confirm=True
        )
        transfer_money.check_alert_message_and_accept(BankAlert.SUCCESSFULLY_TRANSFERRED)

        balance_account = api_manager.user_steps.get_all_accounts(user_request)
        assert get_balance_account(balance_account, acc2.id) == amount

    @pytest.mark.user_session(2)
    @pytest.mark.browsers('chromium')
    def test_user_can_transfer_money_any(
            self,
            page: Page,
            api_manager: ApiManager,
    ):
        user_1: CreateUserRequest = SessionStorage.get_user(0)
        user_2: CreateUserRequest = SessionStorage.get_user(1)
        user_account_1 = api_manager.user_steps.create_account(user_1)
        user_account_2 = api_manager.user_steps.create_account(user_2)

        amount = RandomData.get_deposit_amount()
        api_manager.deposit_steps.deposit(user_1, DepositMoneyRequest(id=user_account_1.id, balance=max_deposit_value()))

        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money(
            account=user_account_1.id,
            recipient_account=user_account_2.accountNumber,
            amount=amount,
            confirm=True
        )
        transfer_money.check_alert_message_and_accept(BankAlert.SUCCESSFULLY_TRANSFERRED)

        balance_account = api_manager.user_steps.get_all_accounts(user_2)
        assert get_balance_account(balance_account, user_account_2.id) == amount

    @pytest.mark.user_session(2)
    @pytest.mark.browsers('chromium')
    def test_transfer_user_when_edit_name(
            self,
            page: Page,
            api_manager: ApiManager,
    ):
        user_1: CreateUserRequest = SessionStorage.get_user(0)
        user_2: CreateUserRequest = SessionStorage.get_user(1)
        user_account_1 = api_manager.user_steps.create_account(user_1)
        user_account_2 = api_manager.user_steps.create_account(user_2)
        api_manager.customer_steps.update_customer_name(user_2, CustomerProfileRequest(name=RandomData.get_profile_username()))

        api_manager.deposit_steps.deposit(user_1, DepositMoneyRequest(id=user_account_1.id, balance=max_deposit_value()))
        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money(
            account=user_account_1.id,
            recipient_account=user_account_2.accountNumber,
            amount=RandomData.get_deposit_amount(),
            confirm=True
        )
        transfer_money.check_alert_message_and_accept(BankAlert.RECIPIENT_NAME_DOESNT_MATCH_THE_REGISTERED_NAME)

        balance_account = api_manager.user_steps.get_all_accounts(user_2)
        assert get_balance_account(balance_account, user_account_2.id) == 0

    @pytest.mark.user_session(1)
    @pytest.mark.browsers('chromium')
    def test_transfer_page_empty_fields(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money()
        transfer_money.check_alert_message_and_accept(BankAlert.PLEASE_FILL_FIELDS)

    @pytest.mark.user_session(1)
    @pytest.mark.browsers('chromium')
    def test_transfer_page_invalid_amount(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        acc1 = api_manager.user_steps.create_account(user_request)
        acc2 = api_manager.user_steps.create_account(user_request)
        amount = RandomData.get_deposit_amount()
        api_manager.deposit_steps.deposit(user_request, DepositMoneyRequest(id=acc1.id, balance=max_deposit_value()))

        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money(
            account=acc1.id,
            recipient_account=acc2.accountNumber,
            amount=max_deposit_value()+amount,
            confirm=True
        )
        transfer_money.check_alert_message_and_accept(BankAlert.INVALID_AMOUNT_OR_ACCOUNT)

        balance_account = api_manager.user_steps.get_all_accounts(user_request)
        assert get_balance_account(balance_account, acc2.id) == 0

    @pytest.mark.user_session(1)
    @pytest.mark.browsers('chromium')
    def test_transfer_page_invalid_account(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        acc1 = api_manager.user_steps.create_account(user_request)
        amount = RandomData.get_deposit_amount()
        api_manager.deposit_steps.deposit(user_request, DepositMoneyRequest(id=acc1.id, balance=max_deposit_value()))

        transfer_money = TransferMoney(page).open()
        expect(transfer_money.transfer_text).to_be_visible()
        transfer_money.transfer_money(
            account=acc1.id,
            recipient_account=str(RandomData.get_invalid_account_id()),
            amount=max_deposit_value() + amount,
            confirm=True
        )
        transfer_money.check_alert_message_and_accept(BankAlert.NO_USER_FOUND_WITH_THIS_ACCOUNT_NUMBER)

