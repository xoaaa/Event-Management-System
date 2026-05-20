from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from domain.refund.refund import Refund


@dataclass
class RefundDTO:
    id: UUID
    booking_id: UUID
    ticket_id: UUID
    requester_id: UUID
    amount: Decimal
    currency: str
    status: str
    rejection_reason: Optional[str]

    @staticmethod
    def from_domain(refund: Refund) -> "RefundDTO":
        return RefundDTO(
            id=refund.id,
            booking_id=refund.booking_id,
            ticket_id=refund.ticket_id,requester_id=refund.requester_id,
            amount=refund.amount.amount,
            currency=refund.amount.currency,
            status=refund.status.value,
            rejection_reason=refund.rejection_reason,
        )