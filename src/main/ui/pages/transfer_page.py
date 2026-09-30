from src.main.ui.pages.base_page import BasePage


class TransferMoney(BasePage):

    @property
    def transfer_text(self):
        return self.page.get_by_text("🔄 Make a Transfer")

    @property
    def transfer_button(self):
        return self.page.get_by_role("button", name="🚀 Send Transfer")

    @property
    def transfer_again_button(self):
        return self.page.get_by_role("button", name="🔁 Transfer Again")

    def url(self):
        return "/transfer"

    def transfer_money(
            self,
            account: int = '',
            recipient_name: str = '',
            recipient_account: str = '',
            amount: float = '',
            confirm: bool = False
    ):
        """
        Метод заполняющий форму перевода ДС

        :param account: Счет с которого переводим деньги
        :param recipient_name: Имя получателя
        :param recipient_account: Номер счёта получателя
        :param amount: Сумма
        :param confirm: чек бокс Confirm details are correct
        :return:
        """
        self.select_account().click()
        self.select_account().select_option(str(account))

        self.page.get_by_placeholder('Enter recipient name').clear()
        self.page.get_by_placeholder('Enter recipient name').fill(recipient_name)

        self.page.get_by_placeholder('Enter recipient account number').clear()
        self.page.get_by_placeholder('Enter recipient account number').fill(recipient_account)

        self.page.get_by_placeholder('Enter amount').clear()
        self.page.get_by_placeholder('Enter amount').fill(str(amount))
        self.page.locator('#confirmCheck').click() if confirm else ...
        self.transfer_button.click()
        return self

    # Тест на валидацию, если ещё не меняли имя, то одна плашка, когда поменяли, другая
