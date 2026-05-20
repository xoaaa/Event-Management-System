import uuid
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from domain.booking.repositories.i_booking_repository import IBookingRepository
from domain.refund.refund import Refund
from domain.refund.repositories.i_refund_repository import IRefundRepository
from domain.shared.value_objects.money import Money


@dataclass
class RequestRefundCommand:
    booking_id: UUID
    ticket_id: UUID
    requester_id: UUID
    amount: Decimal
    currency: str

class RequestRefundCommandHandler:
    def _init_(
        self,
        booking_repository: IBookingRepository,
        refund_repository: IRefundRepository,
    ) -> None:
        self._booking_repository = booking_repository
        self._refund_repository = refund_repository

    def handle(self, command: RequestRefundCommand) -> UUID:
        booking = self._booking_repository.find_by_id(command.booking_id)
        if booking is None:
            raise ValueError(f"Booking '{command.booking_id}' not found.")
        ticket = next(
            (t for t in booking.tickets if t.id == command.ticket_id), None
        )
        if ticket is None:
            raise ValueError(f"Ticket '{command.ticket_id}' not found in booking.")
        refund = Refund(
            id=uuid.uuid4(), booking_id=command.booking_id,
            ticket_id=command.ticket_id,
            requester_id=command.requester_id,
            amount=Money(command.amount, command.currency),
            ticket_is_checked_in=ticket.is_checked_in,
        )
        self._refund_repository.save(refund)
        return refund.id