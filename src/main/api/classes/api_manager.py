from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, created_object: list):
        self.admin_steps = AdminSteps(created_object)
        self.user_steps = UserSteps(created_object)