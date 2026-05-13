import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...shared.interfaces.aggregate_root import AggregateRoot
from ...shared.value_objects.money import Money
from ...shared.value_objects.ticket_code import TicketCode
from .booking_status import BookingStatus
from .ticket import Ticket
from ..events.ticket_reserved import TicketReserved
from ..events.booking_paid import BookingPaid
from ..events.booking_expired import BookingExpired
from ..events.ticket_checked_in import TicketCheckedIn


class Booking(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        booker_id: UUID,
        quantity: int,
        unit_price: Money,
        payment_deadline: datetime,
    ) -> None:
        super().__init__()

        if quantity <= 0:
            raise ValueError("Booking quantity must be greater than zero.")

        self._id = id
        self._event_id = event_id
        self._ticket_category_id = ticket_category_id
        self._booker_id = booker_id
        self._quantity = quantity
        self._unit_price = unit_price
        self._total_price: Money = unit_price.multiply(quantity)
        self._payment_deadline = payment_deadline
        self._status: BookingStatus = BookingStatus.PENDING_PAYMENT
        self._tickets: List[Ticket] = []

        self._add_domain_event(TicketReserved(
            booking_id=self._id,
            event_id=self._event_id,
            ticket_category_id=self._ticket_category_id,
            booker_id=self._booker_id,
            quantity=self._quantity,
        ))

    # ------------------------------------------------------------------ #
    #  Commands                                                            #
    # ------------------------------------------------------------------ #

    def pay(self, paid_amount: Money, paid_at: datetime) -> None:
        if self._status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("Only a pending payment booking can be paid.")
        if paid_at > self._payment_deadline:
            raise ValueError("Payment deadline has already passed.")
        if paid_amount != self._total_price:
            raise ValueError(
                f"Payment amount {paid_amount} does not match "
                f"the total booking price {self._total_price}."
            )

        self._status = BookingStatus.PAID

        for _ in range(self._quantity):
            ticket = Ticket(
                id=uuid.uuid4(),
                booking_id=self._id,
                ticket_category_id=self._ticket_category_id,
                ticket_code=TicketCode.generate(),
            )
            self._tickets.append(ticket)

        self._add_domain_event(BookingPaid(
            booking_id=self._id,
            event_id=self._event_id,
        ))

    def expire(self) -> None:
        if self._status == BookingStatus.PAID:
            raise ValueError("A paid booking cannot expire.")
        if self._status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("Only a pending payment booking can expire.")

        self._status = BookingStatus.EXPIRED
        self._add_domain_event(BookingExpired(
            booking_id=self._id,
            event_id=self._event_id,
        ))

    def check_in_ticket(self, ticket_id: UUID) -> None:
        ticket = self._find_ticket(ticket_id)
        if ticket is None:
            raise ValueError(f"Ticket '{ticket_id}' not found in this booking.")

        ticket.check_in()

        self._add_domain_event(TicketCheckedIn(
            booking_id=self._id,
            ticket_id=ticket_id,
            ticket_code=ticket.ticket_code,
        ))

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _find_ticket(self, ticket_id: UUID) -> Optional[Ticket]:
        for ticket in self._tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    # ------------------------------------------------------------------ #
    #  Properties                                                          #
    # ------------------------------------------------------------------ #

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def event_id(self) -> UUID:
        return self._event_id

    @property
    def ticket_category_id(self) -> UUID:
        return self._ticket_category_id

    @property
    def booker_id(self) -> UUID:
        return self._booker_id

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def unit_price(self) -> Money:
        return self._unit_price

    @property
    def total_price(self) -> Money:
        return self._total_price

    @property
    def payment_deadline(self) -> datetime:
        return self._payment_deadline

    @property
    def status(self) -> BookingStatus:
        return self._status

    @property
    def tickets(self) -> List[Ticket]:
        return list(self._tickets)