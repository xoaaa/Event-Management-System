from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from domain.booking.entities.ticket import Ticket
from domain.booking.entities.booking import Booking


@dataclass
class TicketDTO:
    id: UUID
    booking_id: UUID
    ticket_category_id: UUID
    ticket_code: str
    status: str

    @staticmethod
    def from_domain(ticket: Ticket) -> "TicketDTO":
        return TicketDTO(
            id=ticket.id,
            booking_id=ticket.booking_id,
            ticket_category_id=ticket.ticket_category_id,
            ticket_code=ticket.ticket_code.value,
            status=ticket.status.value,
        )


@dataclass
class BookingDTO:
    id: UUID
    event_id: UUID
    ticket_category_id: UUID
    booker_id: UUID
    quantity: int
    unit_price_amount: Decimal
    unit_price_currency: str
    total_price_amount: Decimal
    total_price_currency: str
    payment_deadline: datetime
    status: str
    tickets: List[TicketDTO]

    @staticmethod
    def from_domain(booking: Booking) -> "BookingDTO":
        return BookingDTO(
            id=booking.id,
            event_id=booking.event_id,
            ticket_category_id=booking.ticket_category_id,
            booker_id=booking.booker_id,
            quantity=booking.quantity,
            unit_price_amount=booking.unit_price.amount,
            unit_price_currency=booking.unit_price.currency,
            total_price_amount=booking.total_price.amount,
            total_price_currency=booking.total_price.currency,
            payment_deadline=booking.payment_deadline,
            status=booking.status.value,
            tickets=[TicketDTO.from_domain(t) for t in booking.tickets],
        )