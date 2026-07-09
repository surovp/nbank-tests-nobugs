import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.usefixtures("api_manager", 'user_request')
    def test_create_account(self, user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.user_steps.create_account(user_request)


