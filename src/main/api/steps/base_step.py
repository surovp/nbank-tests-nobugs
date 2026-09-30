from typing import List, Any

from src.main.allure_step_proxy import AllureStepProxy


class BaseSteps(AllureStepProxy):
    def __init__(self, created_objects: List[Any]):
        self.created_objects = created_objects
