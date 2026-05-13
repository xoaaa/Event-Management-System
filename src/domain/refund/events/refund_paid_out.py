from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent
from ...shared.value_objects.money import Money


class RefundPaidOut(DomainEvent):
    def __init__(self, refund_id: UUID, booking_id: UUID, amount: Money) -> None:
        super().__init__()
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.amount = amount