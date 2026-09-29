from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.customer_steps import CustomerSteps
from src.main.api.steps.deposit_steps import DepositSteps
from src.main.api.steps.transfer_steps import TransferSteps
from src.main.api.steps.user_steps import UserSteps
from src.main.api.steps.database_steps import DataBaseSteps


class ApiManager:
    def __init__(self, created_object: list):
        self.admin_steps = AdminSteps(created_object)
        self.user_steps = UserSteps(created_object)
        self.deposit_steps = DepositSteps(created_object)
        self.transfer_steps = TransferSteps(created_object)
        self.customer_steps = CustomerSteps(created_object)
        self.database_steps = DataBaseSteps
