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
    def request_returns_bad_request(error_value: list, error_key: str | None = None) -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

            if isinstance(error_value, (list, tuple, set)):
                expected_messages = error_value
            else:
                expected_messages = [error_value]

            if error_key:
                actual = response.json().get(error_key)

                if actual is None:
                    raise AssertionError(
                        f"Поле {error_key!r} отсутствует в ответе: {response.text}"
                    )

                if isinstance(actual, list):
                    actual_messages = actual
                else:
                    actual_messages = [actual]

                for expected in expected_messages:
                    assert expected in actual_messages, (
                        f"Ожидалось сообщение {expected!r} для поля {error_key!r}, "
                        f"но получено: {actual_messages}"
                    )
            else:
                body = response.text.strip()
                for expected in expected_messages:
                    assert str(expected) in body, (
                        f"Ожидалось сообщение {expected!r} в теле ответа, "
                        f"но получено: {body!r}"
                    )
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
    MIN_DEPOSIT_AMOUNT = 'must be greater than 0'
    MAX_DEPOSIT_AMOUNT = 'Deposit amount exceeds the 5000 limit'


class TransferErrors(str, Enum):
    INVALID_TRANSFER = 'Invalid transfer: insufficient funds or invalid accounts'
    MIN_TRANSFER_AMOUNT = 'must be greater than 0'
    MAX_TRANSFER_AMOUNT = 'Transfer amount cannot exceed 10000'


class CustomerErrors(str, Enum):
    INVALID_CUSTOMER_NAME = 'Name must contain two words with letters only'
    REGEX_FORMAT = "must match \"^[\\w\\.\\-]+$\""
    LEN_3_TO_15 = "size must be between 3 and 15"
    NO_EMPTY = "must not be blank"
