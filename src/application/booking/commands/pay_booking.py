from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from domain.booking.repositories.i_booking_repository import IBookingRepository
from domain.shared.value_objects.money import Money


@dataclass
class PayBookingCommand:
    booking_id: UUID
    paid_amount: Decimal
    paid_currency: str
    paid_at: datetime

class PayBookingCommandHandler:
    def _init_(self, booking_repository: IBookingRepository) -> None:
        self._booking_repository = booking_repository

    def handle(self, command: PayBookingCommand) -> None:
        booking = self._booking_repository.find_by_id(command.booking_id)
        if booking is None:
            raise ValueError(f"Booking '{command.booking_id}' not found.")
        booking.pay(
            paid_amount=Money(command.paid_amount, command.paid_currency),
            paid_at=command.paid_at,
        )
        self._booking_repository.save(booking)