from typing import Optional
from uuid import UUID

from ..shared.interfaces.aggregate_root import AggregateRoot
from ..shared.value_objects.money import Money
from .refund_status import RefundStatus
from .events.refund_requested import RefundRequested
from .events.refund_approved import RefundApproved
from .events.refund_rejected import RefundRejected
from .events.refund_paid_out import RefundPaidOut


class Refund(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        booking_id: UUID,
        ticket_id: UUID,
        requester_id: UUID,
        amount: Money,
        ticket_is_checked_in: bool,
    ) -> None:
        super().__init__()

        if ticket_is_checked_in:
            raise ValueError(
                "Refund cannot be requested for a ticket that has already been checked in."
            )

        self._id = id
        self._booking_id = booking_id
        self._ticket_id = ticket_id
        self._requester_id = requester_id
        self._amount = amount
        self._status: RefundStatus = RefundStatus.REQUESTED
        self._rejection_reason: Optional[str] = None

        self._add_domain_event(RefundRequested(
            refund_id=self._id,
            booking_id=self._booking_id,
            ticket_id=self._ticket_id,
            requester_id=self._requester_id,
            amount=self._amount,
        ))

    def approve(self) -> None:
        if self._status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be approved when it is in Requested status.")
        self._status = RefundStatus.APPROVED
        self._add_domain_event(RefundApproved(
            refund_id=self._id,
            booking_id=self._booking_id,
        ))

    def reject(self, reason: str) -> None:
        if self._status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be rejected when it is in Requested status.")
        if not reason or not reason.strip():
            raise ValueError("Rejection reason cannot be empty.")
        self._rejection_reason = reason
        self._status = RefundStatus.REJECTED
        self._add_domain_event(RefundRejected(
            refund_id=self._id,
            booking_id=self._booking_id,
            reason=reason,
        ))

    def mark_as_paid_out(self) -> None:
        if self._status != RefundStatus.APPROVED:
            raise ValueError("Refund can only be paid out when it is in Approved status.")
        self._status = RefundStatus.PAID_OUT
        self._add_domain_event(RefundPaidOut(
            refund_id=self._id,
            booking_id=self._booking_id,
            amount=self._amount,
        ))

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def booking_id(self) -> UUID:
        return self._booking_id

    @property
    def ticket_id(self) -> UUID:
        return self._ticket_id

    @property
    def requester_id(self) -> UUID:
        return self._requester_id

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def status(self) -> RefundStatus:
        return self._status

    @property
    def rejection_reason(self) -> Optional[str]:
        return self._rejection_reason