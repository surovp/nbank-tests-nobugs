from typing import TypeVar, Optional
import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest


T = TypeVar('T', bound=BaseModel)


class _NoOpTracker:
    """Заглушка, когда coverage отключён. Декоратор не меняет функцию. Необходимо для локального запуска тестов"""
    def track_coverage_requests(self, *_args, **_kwargs):
        def decorator(func):
            return func
        return decorator


try:
    from swagger_coverage_tool import SwaggerCoverageTracker
    tracker = SwaggerCoverageTracker(service="nbank-api")
except Exception as _e:
    print(f"⚠️  Swagger coverage disabled: {_e}")
    tracker = _NoOpTracker()


class CrudRequester(HttpRequest):
    @property
    def base_url(self) -> str:
        return f"{Config.get('server')}{Config.get('api_version')}"

    def _coverage_path(self, id: int | None = None) -> str:
        path = f"/api{Config.get('api_version')}{self.endpoint.value.url}"
        return f"{path}/{{id}}" if id is not None else path

    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''

        @tracker.track_coverage_requests(self._coverage_path())
        def send_request() -> requests.Response:
            return requests.post(
                url=f'{self.base_url}{self.endpoint.value.url}',
                headers=self.request_spec,
                json=body
            )

        response = send_request()
        self.response_spec(response)
        return response

    def put(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''

        @tracker.track_coverage_requests(self._coverage_path(id))
        def send_request() -> requests.Response:

            return requests.put(
                url=f'{self.base_url}{self.endpoint.value.url}',
                headers=self.request_spec,
                json=body,
            )
        response = send_request()
        self.response_spec(response)
        return response

    def get(self, model: Optional[BaseModel] = None, id: Optional[int] = None):

        @tracker.track_coverage_requests(self._coverage_path(id))
        def send_request() -> requests.Response:
            return requests.get(
                url=f'{self.base_url}{self.endpoint.value.url}{("/" + str(id)) if id is not None else ""}',
                headers=self.request_spec
            )

        response = send_request()
        self.response_spec(response)
        return response

    def update(self, model: BaseModel, id: int):
        ...

    def delete(self, id: int) -> requests.Response:

        @tracker.track_coverage_requests(self._coverage_path(id))
        def send_request() -> requests.Response:
            return requests.delete(
                url=f'{self.base_url}{self.endpoint.value.url}/{id}',
                headers=self.request_spec
            )

        response = send_request()
        self.response_spec(response)
        return response
