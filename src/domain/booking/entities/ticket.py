from enum import Enum
from uuid import uuid4
from src.domain.shared.value_objects.ticket_code import TicketCode


class TicketStatus(str, Enum):
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"
    REFUND_REQUIRED = "RefundRequired"


class Ticket:
    def __init__(
        self,
        id: str,
        booking_id: str,
        ticket_category_id: str,
        code: TicketCode,
        status: TicketStatus = TicketStatus.ACTIVE,
    ):
        self.id = id
        self.booking_id = booking_id
        self.ticket_category_id = ticket_category_id
        self.code = code
        self.status = status

    @classmethod
    def create(cls, booking_id: str, ticket_category_id: str) -> "Ticket":
        return cls(
            id=str(uuid4()),
            booking_id=booking_id,
            ticket_category_id=ticket_category_id,
            code=TicketCode.generate(),
        )

    def check_in(self) -> None:
        if self.status == TicketStatus.CHECKED_IN:
            raise ValueError("Ticket has already been checked in")
        if self.status != TicketStatus.ACTIVE:
            raise ValueError("Only active tickets can be checked in")
        self.status = TicketStatus.CHECKED_IN

    def cancel(self) -> None:
        self.status = TicketStatus.CANCELLED

    def mark_refund_required(self) -> None:
        self.status = TicketStatus.REFUND_REQUIRED

    @property
    def is_checked_in(self) -> bool:
        return self.status == TicketStatus.CHECKED_IN
