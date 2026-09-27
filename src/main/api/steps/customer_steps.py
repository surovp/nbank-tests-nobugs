from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.customer_profile_request import CustomerProfileRequest
from src.main.api.models.customer_profile_response import CustomerResponse
from src.main.api.models.get_customer_profile import GetCustomerProfile
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_step import BaseSteps


class CustomerSteps(BaseSteps):

    def update_customer_name(self, user_request: CreateUserRequest, customer_request: CustomerProfileRequest):
        customer_response: CustomerResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.EDIT_CUSTOMER_NAME,
            ResponseSpecs.request_returns_ok()
        ).put(customer_request)

        customer_profile_response: GetCustomerProfile = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.CUSTOMER_PROFILE,
            ResponseSpecs.request_returns_ok()
        ).get()

        assert customer_response.name == customer_profile_response.name
        return customer_response

    def update_invalid_customer_name(
            self,
            user_request: CreateUserRequest,
            customer_request: CustomerProfileRequest,
            error_value: str,
            error_key: None = None
    ):
        CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.EDIT_CUSTOMER_NAME,
            ResponseSpecs.request_returns_bad_request(error_value, error_key)
        ).put(customer_request)

        customer_profile_response: GetCustomerProfile = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.CUSTOMER_PROFILE,
            ResponseSpecs.request_returns_ok()
        ).get()

        assert customer_profile_response.name is None
