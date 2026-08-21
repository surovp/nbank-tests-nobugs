import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.check_accounts_change(delta=1)
    def test_create_account(self, user_request: CreateUserRequest, api_manager: ApiManager):
        created_account = api_manager.user_steps.create_account(user_request)
        assert created_account.balance == 0

