from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from application.booking.commands.create_booking import CreateBookingCommand
from application.booking.commands.pay_booking import PayBookingCommand
from application.booking.commands.expire_booking import ExpireBookingCommand
from application.booking.queries.get_booking_by_id import GetBookingByIdQuery
from application.booking.dtos.booking_dto import BookingDTO

class IBookingApplicationService(ABC):

    @abstractmethod
    def create_booking(self, command: CreateBookingCommand) -> UUID:
        """Create a new booking and return its ID."""
        ...

    @abstractmethod
    def pay_booking(self, command: PayBookingCommand) -> None:
        """Mark a booking as paid."""
        ...

    @abstractmethod
    def expire_booking(self, command: ExpireBookingCommand) -> None:
        """Expire a pending payment booking."""
        ...

    @abstractmethod
    def get_booking_by_id(self, query: GetBookingByIdQuery) -> Optional[BookingDTO]:
        """Return a BookingDTO by ID, or None if not found."""
        ...