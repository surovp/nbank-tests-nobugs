from typing import Callable
from http import HTTPStatus
from requests import Response


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
    def request_returns_bad_request(error_key: str, error_value: str) -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
            assert error_value in response.json().get(error_key)

        return check