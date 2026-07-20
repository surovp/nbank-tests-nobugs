import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.customer_profile_request import CustomerProfileRequest


@pytest.mark.api
class TestCustomerProfile:

    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.parametrize(
        argnames='name',
        argvalues=[
            'Ivan Ivanov',
            'ivan ivanov',
            'IVAN IVANOV',
            'ivAn ivanoV',
        ]
    )
    def test_customer_name(self, user_request: CreateUserRequest, api_manager: ApiManager, name):
        api_manager.user_steps.create_account(user_request)
        api_manager.customer_steps.update_customer_name(user_request, CustomerProfileRequest(name=name))

    @pytest.mark.usefixtures("api_manager", 'user_request')
    @pytest.mark.parametrize(
        argnames='name',
        argvalues=[
            'Ivan',
            'Ivan Ivanov Ivanovich',
            'Ivan',
            'Ivan  Ivanov',
            ' Ivan Ivanov',
            'Ivan Ivnov ',
            'Ivan1 Ivanov2'
            'Iv@n Ivanov',
            'Ivan-van Ivanov',
            "D'Ivan Ivanov",
            "",
            " ",
            'Иван Иванов',
            'Ivan Иванов',
        ]
    )
    def test_customer_invalid_name(self, user_request: CreateUserRequest, api_manager: ApiManager, name):
        api_manager.user_steps.create_account(user_request)
        api_manager.customer_steps.update_invalid_customer_name(
            user_request, CustomerProfileRequest(name=name), 'Name must contain two words with letters only'
        )
