import time
from typing import List
from src.main.api.models.account_response import AccountsListResponse


def get_balance_account(list_accounts: List[AccountsListResponse], acc_id: int) -> int | float:
    res = next((acc.balance for acc in list_accounts if acc.id == acc_id), 0)
    return res


def get_balance_in_cents(list_accounts: List[AccountsListResponse], acc_id: int) -> int:
    """Возвращает баланс в копейках (целое) — для точных сравнений."""
    return round(get_balance_account(list_accounts, acc_id) * 100)


def get_summ_in_cents(amount: int | float) -> int:
    return round(amount * 100)


def max_deposit_value() -> float:
    return 5000.00


def wait_until(condition, timeout: int = 5, interval: float = 0.5):
    """Ожидает, пока условие не станет истинным"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return True
        time.sleep(interval)
    return False


def test_util():
    print('Тестирование нового ямл файла')
