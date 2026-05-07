from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class EventCancelled(DomainEvent):
    def __init__(self, event_id: UUID) -> None:
        super().__init__()
        self.event_id = event_id