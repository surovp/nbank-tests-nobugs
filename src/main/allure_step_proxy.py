from functools import wraps
from typing import Any

import allure


class AllureStepProxy:
    _allure_step_skip = frozenset({"url"})

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)

        if name.startswith("_") or name in self._allure_step_skip or not callable(attr):
            return attr

        @wraps(attr)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with allure.step(f"{self.__class__.__name__}.{name}"):
                return attr(*args, **kwargs)

        return wrapper