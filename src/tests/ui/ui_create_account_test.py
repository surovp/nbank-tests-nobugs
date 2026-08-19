import pytest
from playwright.sync_api import expect, Page
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard


@pytest.mark.ui
class TestCreateAccount:
    @pytest.mark.user_session(1)
    def test_user_can_create_account(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        user_dashboard = UserDashboard(page).open()
        expect(user_dashboard.welcome_text).to_be_visible()

        user_dashboard = user_dashboard.create_new_account()
        user_dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)
        user_accounts = api_manager.user_steps.get_all_accounts(user_request)

        assert len(user_accounts) == 1
        assert user_accounts[0] and user_accounts[0].balance == 0