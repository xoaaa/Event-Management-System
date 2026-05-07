from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class DomainEvent(ABC):
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)


class AggregateRoot:
    def __init__(self):
        self._domain_events: list[DomainEvent] = []

    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
