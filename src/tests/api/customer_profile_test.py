import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.comparison.dao_and_model_assertions import DaoAndModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.customer_profile_request import CustomerProfileRequest
from src.main.api.specs.response_specs import CustomerErrors


@pytest.mark.api
@pytest.mark.api_version("with_database")
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
        created = api_manager.customer_steps.update_customer_name(user_request, CustomerProfileRequest(name=name))

        dao_name = api_manager.database_steps.get_name_by_customer_name(created.customer.name)
        DaoAndModelAssertions.assert_that(created.customer, dao_name).match()

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
        api_manager.customer_steps.update_invalid_customer_name(
            user_request, CustomerProfileRequest(name=name), CustomerErrors.INVALID_CUSTOMER_NAME.value
        )

        user_dao = api_manager.database_steps.find_name_by_customer_name(name)
        assert user_dao is None, f"User '{name}' should NOT exist in DB after invalid create, but was found: {user_dao}"