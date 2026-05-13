from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class TicketReserved(DomainEvent):
    def __init__(
        self,
        booking_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        booker_id: UUID,
        quantity: int,
    ) -> None:
        super().__init__()
        self.booking_id = booking_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.booker_id = booker_id
        self.quantity = quantity