from src.main.ui.pages.base_page import BasePage


class DepositMoney(BasePage):

    @property
    def deposit_text(self):
        return self.page.get_by_text("💰 Deposit Money")

    @property
    def deposit_button(self):
        return self.page.get_by_role("button", name="💵 Deposit")

    def url(self):
        return "/deposit"

    def default_option_choose_an_account(self):
        return

    def deposit_money(self, amount: float = "", account: int = ""):
        """
        Метод заполняет поля для пополнения счёта, по дефолту None
        :param amount: Сумма пополнения
        :param account: Номер счёта
        :return:
        """
        self.select_account().click()
        self.select_account().select_option(str(account))
        self.page.get_by_placeholder('Enter amount').fill(str(amount))
        self.deposit_button.click()
        return self
