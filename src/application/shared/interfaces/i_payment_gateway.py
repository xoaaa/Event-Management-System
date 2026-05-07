from abc import ABC, abstractmethod
from src.domain.shared.value_objects.money import Money


class IPaymentGateway(ABC):
    @abstractmethod
    async def process_payment(self, booking_id: str, amount: Money) -> str:
        """Returns a payment reference string."""
        ...
