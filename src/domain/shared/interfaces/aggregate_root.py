from typing import List
from .domain_event import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self._domain_events: List[DomainEvent] = []

    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events