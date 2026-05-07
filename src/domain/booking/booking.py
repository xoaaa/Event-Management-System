from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from src.domain.shared.interfaces.aggregate_root import AggregateRoot
from src.domain.shared.value_objects.money import Money
from src.domain.booking.entities.ticket import Ticket
from src.domain.booking.events.booking_domain_events import (
    TicketReserved, BookingPaid, BookingExpired,
)

PAYMENT_DEADLINE_MINUTES = 15


class BookingStatus(str, Enum):
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"


class Booking(AggregateRoot):
    def __init__(
        self,
        id: str,
        customer_id: str,
        event_id: str,
        ticket_category_id: str,
        quantity: int,
        total_price: Money,
        payment_deadline: datetime,
        status: BookingStatus = BookingStatus.PENDING_PAYMENT,
        tickets: list[Ticket] | None = None,
    ):
        super().__init__()
        self.id = id
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.total_price = total_price
        self.payment_deadline = payment_deadline
        self.status = status
        self._tickets: list[Ticket] = tickets or []

    @classmethod
    def create(
        cls,
        id: str,
        customer_id: str,
        event_id: str,
        ticket_category_id: str,
        quantity: int,
        unit_price: Money,
        service_fee: Optional[Money] = None,
    ) -> "Booking":
        if quantity <= 0:
            raise ValueError("Ticket quantity must be greater than zero")
        total_price = unit_price.multiply(quantity)
        if service_fee:
            total_price = total_price.add(service_fee)
        if total_price.amount < 0:
            raise ValueError("Total price cannot be negative")
        payment_deadline = datetime.utcnow() + timedelta(minutes=PAYMENT_DEADLINE_MINUTES)
        booking = cls(
            id=id, customer_id=customer_id, event_id=event_id,
            ticket_category_id=ticket_category_id, quantity=quantity,
            total_price=total_price, payment_deadline=payment_deadline,
        )
        booking._add_domain_event(TicketReserved(booking_id=id))
        return booking

    def pay(self, amount_paid: Money) -> None:
        if self.status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("Booking is not pending payment")
        if datetime.utcnow() > self.payment_deadline:
            raise ValueError("Payment deadline has passed")
        if amount_paid != self.total_price:
            raise ValueError("Payment amount does not match booking total")
        self.status = BookingStatus.PAID
        for _ in range(self.quantity):
            self._tickets.append(
                Ticket.create(
                    booking_id=self.id,
                    ticket_category_id=self.ticket_category_id,
                )
            )
        self._add_domain_event(BookingPaid(booking_id=self.id))

    def expire(self) -> None:
        if self.status == BookingStatus.PAID:
            raise ValueError("A paid booking cannot be expired")
        if self.status != BookingStatus.PENDING_PAYMENT:
            return
        self.status = BookingStatus.EXPIRED
        self._add_domain_event(BookingExpired(booking_id=self.id))

    def mark_refunded(self) -> None:
        self.status = BookingStatus.REFUNDED
        for ticket in self._tickets:
            ticket.mark_refund_required()

    @property
    def tickets(self) -> list[Ticket]:
        return list(self._tickets)
