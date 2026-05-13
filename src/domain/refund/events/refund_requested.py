from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent
from ...shared.value_objects.money import Money


class RefundRequested(DomainEvent):
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        ticket_id: UUID,
        requester_id: UUID,
        amount: Money,
    ) -> None:
        super().__init__()
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.ticket_id = ticket_id
        self.requester_id = requester_id
        self.amount = amount