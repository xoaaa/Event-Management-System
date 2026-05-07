from abc import ABC, abstractmethod
from typing import Optional
from src.domain.booking.booking import Booking


class IBookingRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Booking]: ...

    @abstractmethod
    async def find_by_customer_and_event(
        self, customer_id: str, event_id: str
    ) -> Optional[Booking]: ...

    @abstractmethod
    async def find_expired_pending(self) -> list[Booking]: ...

    @abstractmethod
    async def save(self, booking: Booking) -> None: ...
