from dataclasses import dataclass
from uuid import UUID

from domain.booking.repositories.i_booking_repository import IBookingRepository


@dataclass
class ExpireBookingCommand:
    booking_id: UUID


class ExpireBookingCommandHandler:
    def __init__(self, booking_repository: IBookingRepository) -> None:
        self._booking_repository = booking_repository

def handle(self, command: ExpireBookingCommand) -> None:
        booking = self._booking_repository.find_by_id(command.booking_id)
        if booking is None:
            raise ValueError(f"Booking '{command.booking_id}' not found.")
        booking.expire()
        self._booking_repository.save(booking)