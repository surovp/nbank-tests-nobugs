from typing import Optional, Any


class FraudMock:
    """
    Конструктор моков для фрод-системы.

    Пример использования:
        # Готовый мок для декоратора
        mock = (FraudMockBuilder()
                .approved()
                .with_risk_score(0.1)
                .build())

        # Expected для TransferResponseFraudCheck
        expected = (FraudMockBuilder()
                    .approved()
                    .build_expected(
                        status="APPROVED",
                        message="Transfer approved and processed immediately"
                    ))
    """

    def __init__(self):
        self._mock = {
            "status": "SUCCESS",
            "decision": "APPROVED",
            "riskScore": 0.2,
            "reason": "Mocked fraud decision",
            "requiresManualReview": False,
            "additionalVerificationRequired": False,
        }

    # ========== Базовые сценарии ==========
    def approved(self) -> "FraudMock":
        """Мок для APPROVED"""
        self._mock.update({
            "status": "SUCCESS",
            "decision": "APPROVED",
            "riskScore": 0.2,
            "reason": "Low risk transaction",
            "requiresManualReview": False,
            "additionalVerificationRequired": False,
        })
        return self

    def manual_review(self) -> "FraudMock":
        """Мок для DECLINED"""
        self._mock.update({
            "status": "SUCCESS",
            "decision": "MANUAL_REVIEW_REQUIRED",
            "riskScore": 0.9,
            "reason": "Suspicious transaction pattern detected",
            "requiresManualReview": False,
            "additionalVerificationRequired": False,
        })
        return self

    def verification_required(self) -> "FraudMock":
        """Мок для REVIEW (ручная проверка)"""
        self._mock.update({
            "status": "SUCCESS",
            "decision": "VERIFICATION_REQUIRED",
            "riskScore": 0.6,
            "reason": "Transaction requires manual review due to unusual amount",
            "requiresManualReview": True,
            "additionalVerificationRequired": True,
        })
        return self

    # ========== Модификаторы ==========

    def with_risk_score(self, score: Optional[float]) -> "FraudMock":
        """Установить риск-скор"""
        self._mock["riskScore"] = score
        return self

    def with_reason(self, reason: str) -> "FraudMock":
        """Установить причину"""
        self._mock["reason"] = reason
        return self

    def with_manual_review(self, required: bool = True) -> "FraudMock":
        """Установить флаг ручной проверки"""
        self._mock["requiresManualReview"] = required
        return self

    def with_verification(self, required: bool = True) -> "FraudMock":
        """Установить флаг дополнительной верификации"""
        self._mock["additionalVerificationRequired"] = required
        return self

    def with_status(self, status: str) -> "FraudMock":
        """Установить статус ответа фрод-системы"""
        self._mock["status"] = status
        return self

    def with_decision(self, decision: str) -> "FraudMock":
        """Установить решение фрод-системы"""
        self._mock["decision"] = decision
        return self

    def with_custom_field(self, key: str, value: Any) -> "FraudMock":
        """Добавить кастомное поле в ответ фрод-системы"""
        self._mock[key] = value
        return self

    # ========== Сборка ==========

    def build(self) -> dict:
        """
        Вернуть готовый мок для декоратора @pytest.mark.fraud_check_mock.

        Returns:
            Словарь с ответом фрод-системы:
            {
                "status": "SUCCESS",
                "decision": "APPROVED",
                "riskScore": 0.2,
                "reason": "Low risk transaction",
                "requiresManualReview": False,
                "additionalVerificationRequired": False,
            }
        """
        return self._mock.copy()

    def build_expected(self, status: str, message: str) -> dict:
        """
        Вернуть ожидаемый ответ TransferResponseFraudCheck на основе мока.

        Args:
            status: Статус перевода (APPROVED/DECLINED/PENDING_REVIEW/ERROR)
            message: Сообщение для клиента

        Returns:
            Словарь для TransferResponseFraudCheck:
            {
                "status": "APPROVED",
                "message": "Transfer approved and processed immediately",
                "fraudRiskScore": 0.2,
                "fraudReason": "Low risk transaction",
                "requiresManualReview": False,
                "requiresVerification": False,
            }
        """
        mock = self._mock
        return {
            "status": status,
            "message": message,
            "fraudRiskScore": mock.get("riskScore"),
            "fraudReason": mock.get("reason"),
            "requiresManualReview": mock.get("requiresManualReview", False),
            "requiresVerification": mock.get("additionalVerificationRequired", False),
        }


# ========== Готовые моки для фрод-системы ==========

FRAUD_APPROVED_MOCK = FraudMock().approved().build()
FRAUD_MANUAL_REVIEW_MOCK = FraudMock().manual_review().build()
FRAUD_VERIFICATION_REQUIRED_MOCK = FraudMock().verification_required().build()

# ========== Готовые expected для TransferResponseFraudCheck ==========

TRANSFER_APPROVED_EXPECTED = FraudMock().approved().build_expected(
    status="APPROVED",
    message="Transfer approved and processed immediately",
)

TRANSFER_MANUAL_REVIEW_EXPECTED = FraudMock().manual_review().build_expected(
    status="MANUAL_REVIEW_REQUIRED",
    message="Transfer requires manual review",
)

TRANSFER_VERIFICATION_REQUIRED_EXPECTED = FraudMock().verification_required().build_expected(
    status="VERIFICATION_REQUIRED",
    message="Additional verification required",
)