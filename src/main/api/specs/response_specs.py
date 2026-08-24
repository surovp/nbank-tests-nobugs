from typing import Callable
from http import HTTPStatus
from requests import Response
from enum import Enum


class ResponseSpecs:
    @staticmethod
    def request_returns_ok() -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text

        return check

    @staticmethod
    def entity_was_created() -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text

        return check

    @staticmethod
    def entity_was_deleted() -> Callable:
        def check(response: Response):
            assert response.status_code in [HTTPStatus.NO_CONTENT, HTTPStatus.OK], response.text

        return check

    @staticmethod
    def request_returns_bad_request(error_value: str, error_key: str | None = None) -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
            print(response.text)
            if error_key:
                assert error_value in response.json().get(error_key)
            else:
                assert error_value in response.text.strip()

        return check

    @staticmethod
    def request_returns_forbidden(error_value: str, error_key: str | None = None) -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
            if error_key:
                assert error_value in response.json().get(error_key)
            else:
                assert error_value in response.text.strip()

        return check



class DepositErrors(str, Enum):
    UNAUTHORIZED_ACCOUNT = 'Unauthorized access to account'
    MIN_DEPOSIT_AMOUNT = 'Deposit amount must be at least 0.01'
    MAX_DEPOSIT_AMOUNT = 'Deposit amount cannot exceed 5000'

class TransferErrors(str, Enum):
    INVALID_TRANSFER = 'Invalid transfer: insufficient funds or invalid accounts'
    MIN_TRANSFER_AMOUNT = 'Transfer amount must be at least 0.01'
    MAX_TRANSFER_AMOUNT = 'Transfer amount cannot exceed 10000'

class CustomerErrors(str, Enum):
    INVALID_CUSTOMER_NAME = 'Name must contain two words with letters only'


