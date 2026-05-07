from enum import Enum
from typing import Optional
from src.domain.shared.interfaces.aggregate_root import AggregateRoot
from src.domain.shared.value_objects.money import Money
from src.domain.refund.events.refund_domain_events import (
    RefundRequested, RefundApproved, RefundRejected, RefundPaidOut,
)


class RefundStatus(str, Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"


class Refund(AggregateRoot):
    def __init__(
        self,
        id: str,
        booking_id: str,
        customer_id: str,
        amount: Money,
        status: RefundStatus = RefundStatus.REQUESTED,
        rejection_reason: Optional[str] = None,
        payment_reference: Optional[str] = None,
    ):
        super().__init__()
        self.id = id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.status = status
        self.rejection_reason = rejection_reason
        self.payment_reference = payment_reference

    @classmethod
    def request(
        cls, id: str, booking_id: str, customer_id: str, amount: Money
    ) -> "Refund":
        refund = cls(id=id, booking_id=booking_id, customer_id=customer_id, amount=amount)
        refund._add_domain_event(RefundRequested(refund_id=id))
        return refund

    def approve(self) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be approved when in Requested status")
        self.status = RefundStatus.APPROVED
        self._add_domain_event(RefundApproved(refund_id=self.id))

    def reject(self, reason: str) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be rejected when in Requested status")
        if not reason or not reason.strip():
            raise ValueError("Rejection reason must be provided")
        self.status = RefundStatus.REJECTED
        self.rejection_reason = reason
        self._add_domain_event(RefundRejected(refund_id=self.id, reason=reason))

    def mark_paid_out(self, payment_reference: str) -> None:
        if self.status != RefundStatus.APPROVED:
            raise ValueError("Refund can only be paid out when in Approved status")
        if not payment_reference or not payment_reference.strip():
            raise ValueError("Payment reference must be provided")
        self.status = RefundStatus.PAID_OUT
        self.payment_reference = payment_reference
        self._add_domain_event(
            RefundPaidOut(refund_id=self.id, payment_reference=payment_reference)
        )
