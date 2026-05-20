from dataclasses import dataclass
from uuid import UUID

from domain.booking.repositories.i_booking_repository import IBookingRepository


@dataclass
class CheckInTicketCommand:
    booking_id: UUID
    ticket_id: UUID


class CheckInTicketCommandHandler:
    def __init__(self, booking_repository: IBookingRepository) -> None:
        self._booking_repository = booking_repository

    def handle(self, command: CheckInTicketCommand) -> None:
        booking = self._booking_repository.find_by_id(command.booking_id)
        if booking is None:
            raise ValueError(f"Booking '{command.booking_id}' not found.")
        booking.check_in_ticket(command.ticket_id)
        self._booking_repository.save(booking)