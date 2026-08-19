import time
from typing import List
from src.main.api.models.account_response import AccountsListResponse


def get_balance_account(list_accounts: List[AccountsListResponse], acc_id: int) -> int | float:
    return next((acc.balance for acc in list_accounts if acc.id == acc_id), 0)

def max_deposit_value() -> float:
    return 5000.00

def wait_until(condition, timeout:int=5, interval:float=0.5):
    """Ожидает, пока условие не станет истинным"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return True
        time.sleep(interval)
    return False