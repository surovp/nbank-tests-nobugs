import time

import pytest
from playwright.sync_api import expect, Page
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.utils.helpers import wait_until
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.profile_page import Profile


@pytest.mark.ui
class TestEditProfile:
    @pytest.mark.user_session(1)
    def test_edit_profile(self, page: Page, user_request: CreateUserRequest, api_manager: ApiManager):
        user_profile = Profile(page).open()
        expect(user_profile.profile_text).to_be_visible()

        name = RandomData.get_profile_username()
        user_profile.edit_profile(name=name)
        user_profile.check_alert_message_and_accept(BankAlert.NAME_UPDATED_SUCCESSFULLY)

        wait_until(lambda: api_manager.user_steps.get_profile(user_request).name == name)

    @pytest.mark.user_session(1)
    @pytest.mark.parametrize(
        argnames='name, alert',
        argvalues=[
            ('', BankAlert.PLEASE_ENTER_VALID_NAME),
            (RandomData.get_username(), BankAlert.NAME_MUST_CONTAIN_TWO_WORDS_WITH_LETTERS_ONLY),
        ]
    )
    def test_edit_profile_invalid_name(
            self,
            name,
            alert,
            page: Page,
            user_request: CreateUserRequest,
            api_manager: ApiManager
    ):
        user_profile = Profile(page).open()
        expect(user_profile.profile_text).to_be_visible()

        user_profile.edit_profile(name=name)
        user_profile.check_alert_message_and_accept(alert)

        assert api_manager.user_steps.get_profile(user_request).name is None

