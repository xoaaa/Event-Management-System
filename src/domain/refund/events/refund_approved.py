from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class RefundApproved(DomainEvent):
    def __init__(self, refund_id: UUID, booking_id: UUID) -> None:
        super().__init__()
        self.refund_id = refund_id
        self.booking_id = booking_id