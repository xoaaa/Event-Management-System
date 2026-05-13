from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class RefundRejected(DomainEvent):
    def __init__(self, refund_id: UUID, booking_id: UUID, reason: str) -> None:
        super().__init__()
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.reason = reason