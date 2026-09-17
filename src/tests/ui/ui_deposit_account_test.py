import pytest
from playwright.sync_api import expect, Page
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.utils.helpers import get_balance_account
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.deposit_page import DepositMoney


@pytest.mark.ui
@pytest.mark.usefixtures("user_session_extension", "browser_match_guard")
class TestDepositAccount:
    @pytest.mark.user_session(1)
    def test_user_can_deposit_account(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        user_account = api_manager.user_steps.create_account(user_request)
        amount = RandomData.get_deposit_amount()

        deposit = DepositMoney(page).open()
        expect(deposit.deposit_text).to_be_visible()
        user_deposit = deposit.deposit_money(account=user_account.id, amount=amount)
        user_deposit.check_alert_message_and_accept(BankAlert.SUCCESS_DEPOSIT)

        balance_account = api_manager.user_steps.get_all_accounts(user_request)
        assert get_balance_account(balance_account, user_account.id) == amount

    @pytest.mark.user_session(1)
    def test_user_no_select_account(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        deposit = DepositMoney(page).open()
        expect(deposit.deposit_text).to_be_visible()
        user_deposit = deposit.deposit_money(amount=RandomData.get_deposit_amount())
        user_deposit.check_alert_message_and_accept(BankAlert.PLEASE_SELECT_ACCOUNT)

    @pytest.mark.user_session(1)
    def test_user_no_input_amount(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        user_account = api_manager.user_steps.create_account(user_request)
        deposit = DepositMoney(page).open()
        expect(deposit.deposit_text).to_be_visible()
        user_deposit = deposit.deposit_money(account=user_account.id)
        user_deposit.check_alert_message_and_accept(BankAlert.PLEASE_ENTER_VALID_AMOUNT)
