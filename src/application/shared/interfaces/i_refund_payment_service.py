from abc import ABC, abstractmethod
from src.domain.shared.value_objects.money import Money


class IRefundPaymentService(ABC):
    @abstractmethod
    async def process_refund(self, refund_id: str, amount: Money, customer_id: str) -> str:
        """Returns a payment reference string."""
        ...
