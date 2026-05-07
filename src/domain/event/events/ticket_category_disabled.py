from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class TicketCategoryDisabled(DomainEvent):
    def __init__(self, event_id: UUID, ticket_category_id: UUID) -> None:
        super().__init__()
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id