from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    async def send_booking_confirmation(self, customer_id: str, booking_id: str) -> None: ...

    @abstractmethod
    async def send_refund_update(self, customer_id: str, refund_id: str, status: str) -> None: ...
