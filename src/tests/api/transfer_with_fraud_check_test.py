import random

import allure
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response_fraud import TransferResponseFraudCheck
from src.main.api.specs.fraud_mock import FRAUD_APPROVED_MOCK, TRANSFER_APPROVED_EXPECTED, \
    FRAUD_VERIFICATION_REQUIRED_MOCK, TRANSFER_VERIFICATION_REQUIRED_EXPECTED, FRAUD_MANUAL_REVIEW_MOCK, \
    TRANSFER_MANUAL_REVIEW_EXPECTED

@pytest.mark.api
@pytest.mark.api_version("with_fraud_check")
@pytest.mark.prepare_users(number=2)
@pytest.mark.prepare_accounts(number=2, deposit=5000)
class TestTransferWithFraudCheck:
    @pytest.mark.parametrize(
        "fraud_mock, expected_data",
        [
            pytest.param(FRAUD_APPROVED_MOCK, TRANSFER_APPROVED_EXPECTED,
                      marks=pytest.mark.fraud_check_mock(
                          port=8080,
                          endpoint=r"/.*",
                          **FRAUD_APPROVED_MOCK)),

            pytest.param(FRAUD_MANUAL_REVIEW_MOCK, TRANSFER_MANUAL_REVIEW_EXPECTED,
                         marks=pytest.mark.fraud_check_mock(
                             port=8080,
                             endpoint=r"/.*",
                             **FRAUD_MANUAL_REVIEW_MOCK
                         )),

            pytest.param(FRAUD_VERIFICATION_REQUIRED_MOCK, TRANSFER_VERIFICATION_REQUIRED_EXPECTED,
                         marks=pytest.mark.fraud_check_mock(
                             port=8080,
                             endpoint=r"/.*",
                             **FRAUD_VERIFICATION_REQUIRED_MOCK))
        ])
    def test_transfer_with_fraud_check(
            self,
            fraud_mock,
            expected_data,
            api_manager: ApiManager,
            prepared_user_accounts: list[PreparedUserAccount],
            fraud_check_mock_server,
    ):
        with allure.step("Prepare sender/receiver accounts (2 accounts with deposit=5000)"):
            sender = prepared_user_accounts[0]
            receiver = prepared_user_accounts[1]

        with allure.step("Transfer with fraud check"):
            transfer_amount = round(random.uniform(0.1, 4999.9), 2)
            transfer_request = TransferMoneyRequest(
                senderAccountId=sender.account.id,
                receiverAccountId=receiver.account.id,
                amount=transfer_amount,
            )
            transfer_response = api_manager.transfer_steps.transfer_with_fraud_check(
                sender.user,
                transfer_request,
            )

        with allure.step("Validate transfer response matches mocked fraud decision"):
            expected = TransferResponseFraudCheck(
                amount=transfer_amount,
                senderAccountId=sender.account.id,
                receiverAccountId=receiver.account.id,
                **expected_data
            )
            ModelAssertions(expected, transfer_response).match()
