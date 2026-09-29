from typing import TypeVar, Optional

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest


T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest):
    @property
    def base_url(self) -> str:
        return f"{Config.get('server')}{Config.get('api_version')}"

    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        response = requests.post(
            url=f'{self.base_url}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body,
        )
        self.response_spec(response)
        return response

    def put(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        response = requests.put(
            url=f'{self.base_url}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body,
        )
        self.response_spec(response)
        return response

    def get(self, model: Optional[BaseModel] = None, id: Optional[int] = None):
        response = requests.get(
            url=f'{self.base_url}{self.endpoint.value.url}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def update(self, model: BaseModel, id: int):
        ...

    def delete(self, id: int) -> requests.Response:
        response = requests.delete(
            url=f'{self.base_url}{self.endpoint.value.url}/{id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
