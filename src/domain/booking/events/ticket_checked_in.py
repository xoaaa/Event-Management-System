from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent
from ...shared.value_objects.ticket_code import TicketCode


class TicketCheckedIn(DomainEvent):
    def __init__(self, booking_id: UUID, ticket_id: UUID, ticket_code: TicketCode) -> None:
        super().__init__()
        self.booking_id = booking_id
        self.ticket_id = ticket_id
        self.ticket_code = ticket_code