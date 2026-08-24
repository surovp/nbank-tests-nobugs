import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.api
class TestCreateUser:
    @pytest.mark.check_all_users_change(delta=1, username_source="create_user_request.username", should_exist=True)
    @pytest.mark.parametrize('create_user_request', [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_valid_user(self, create_user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.admin_steps.create_user(create_user_request)

    @pytest.mark.usefixtures('api_manager')
    @pytest.mark.parametrize(
        argnames='username, password, role, error_key, error_value',
        argvalues=[
            ('', RandomData.get_password(), 'USER', 'username', 'Username cannot be blank'),
            ('qw', RandomData.get_password(), 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('qwertyuiopqwerty', RandomData.get_password(), 'USER', 'username',
             'Username must be between 3 and 15 characters'),
            ('!qgwqg', RandomData.get_password(), 'USER', 'username',
             'Username must contain only letters, digits, dashes, underscores, and dots'),
        ]
    )
    @pytest.mark.check_all_users_change(delta=0, username_source="username", should_exist=False)
    def test_create_invalid_user(
            self,
            api_manager: ApiManager,
            username: str,
            password: str,
            role: str,
            error_key: str,
            error_value: str
    ):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        api_manager.admin_steps.create_invalid_user(create_user_request, error_key, error_value)
