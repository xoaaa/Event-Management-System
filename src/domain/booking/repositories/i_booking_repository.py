from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.booking import Booking


class IBookingRepository(ABC):

    @abstractmethod
    def save(self, booking: Booking) -> None:
        """Persist a new or updated Booking aggregate."""
        ...

    @abstractmethod
    def find_by_id(self, booking_id: UUID) -> Optional[Booking]:
        """Return the Booking with the given id, or None if not found."""
        ...

    @abstractmethod
    def find_all_pending_by_event(self, event_id: UUID) -> List[Booking]:
        """Return all pending payment Bookings for a given event."""
        ...