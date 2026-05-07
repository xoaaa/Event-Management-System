from uuid import UUID

from ...shared.interfaces.domain_event import DomainEvent


class EventCreated(DomainEvent):
    def __init__(self, event_id: UUID, organizer_id: UUID, name: str) -> None:
        super().__init__()
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.name = name