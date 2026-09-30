from playwright.sync_api import Locator

from src.main.allure_step_proxy import AllureStepProxy


class BaseElement(AllureStepProxy):
    def __init__(self, element: Locator):
        self.element: Locator = element

    def find(self, selector: str) -> Locator:
        return self.element.locator(selector)
