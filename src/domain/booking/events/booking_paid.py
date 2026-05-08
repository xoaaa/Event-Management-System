from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class BookingPaid(DomainEvent):
    def __init__(self, booking_id: UUID, event_id: UUID) -> None:
        super().__init__()
        self.booking_id = booking_id
        self.event_id = event_id