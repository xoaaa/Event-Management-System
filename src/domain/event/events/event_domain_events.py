from dataclasses import dataclass
from src.domain.shared.interfaces.aggregate_root import DomainEvent


@dataclass
class EventCreated(DomainEvent):
    aggregate_id: str = ""


@dataclass
class EventPublished(DomainEvent):
    aggregate_id: str = ""


@dataclass
class EventCancelled(DomainEvent):
    aggregate_id: str = ""


@dataclass
class TicketCategoryCreated(DomainEvent):
    aggregate_id: str = ""
    category_id: str = ""


@dataclass
class TicketCategoryDisabled(DomainEvent):
    aggregate_id: str = ""
    category_id: str = ""
