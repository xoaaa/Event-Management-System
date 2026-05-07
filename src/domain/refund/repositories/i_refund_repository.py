from abc import ABC, abstractmethod
from typing import Optional
from src.domain.refund.refund import Refund


class IRefundRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Refund]: ...

    @abstractmethod
    async def find_by_booking_id(self, booking_id: str) -> Optional[Refund]: ...

    @abstractmethod
    async def save(self, refund: Refund) -> None: ...
