from enum import Enum
from typing import Optional
from src.domain.shared.interfaces.aggregate_root import AggregateRoot
from src.domain.shared.value_objects.date_range import DateRange
from src.domain.shared.value_objects.money import Money
from src.domain.event.entities.ticket_category import TicketCategory
from src.domain.event.events.event_domain_events import (
    EventCreated, EventPublished, EventCancelled,
    TicketCategoryCreated, TicketCategoryDisabled,
)


class EventStatus(str, Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class Event(AggregateRoot):
    def __init__(
        self,
        id: str,
        organizer_id: str,
        name: str,
        description: str,
        schedule: DateRange,
        location: str,
        max_capacity: int,
        status: EventStatus = EventStatus.DRAFT,
        ticket_categories: list[TicketCategory] | None = None,
    ):
        super().__init__()
        if max_capacity <= 0:
            raise ValueError("Maximum capacity must be greater than zero")

        self.id = id
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.schedule = schedule
        self.location = location
        self.max_capacity = max_capacity
        self.status = status
        self._ticket_categories: list[TicketCategory] = ticket_categories or []

    @classmethod
    def create(
        cls,
        id: str,
        organizer_id: str,
        name: str,
        description: str,
        schedule: DateRange,
        location: str,
        max_capacity: int,
    ) -> "Event":
        event = cls(
            id=id, organizer_id=organizer_id, name=name,
            description=description, schedule=schedule,
            location=location, max_capacity=max_capacity,
        )
        event._add_domain_event(EventCreated(aggregate_id=id))
        return event

    def publish(self) -> None:
        if self.status == EventStatus.CANCELLED:
            raise ValueError("A cancelled event cannot be published")
        active_categories = [c for c in self._ticket_categories if c.is_active]
        if not active_categories:
            raise ValueError("Event must have at least one active ticket category")
        total_quota = sum(c.quota for c in self._ticket_categories)
        if total_quota > self.max_capacity:
            raise ValueError("Total ticket quota exceeds maximum event capacity")
        self.status = EventStatus.PUBLISHED
        self._add_domain_event(EventPublished(aggregate_id=self.id))

    def cancel(self) -> None:
        if self.status == EventStatus.COMPLETED:
            raise ValueError("A completed event cannot be cancelled")
        if self.status != EventStatus.PUBLISHED:
            raise ValueError("Only a published event can be cancelled")
        self.status = EventStatus.CANCELLED
        for category in self._ticket_categories:
            category.disable()
        self._add_domain_event(EventCancelled(aggregate_id=self.id))

    def add_ticket_category(self, category: TicketCategory) -> None:
        total_quota = sum(c.quota for c in self._ticket_categories) + category.quota
        if total_quota > self.max_capacity:
            raise ValueError("Total ticket quota would exceed maximum event capacity")
        self._ticket_categories.append(category)
        self._add_domain_event(
            TicketCategoryCreated(aggregate_id=self.id, category_id=category.id)
        )

    def disable_ticket_category(self, category_id: str) -> None:
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Cannot disable category of a completed event")
        category = self._find_category_or_raise(category_id)
        category.disable()
        self._add_domain_event(
            TicketCategoryDisabled(aggregate_id=self.id, category_id=category_id)
        )

    def get_lowest_price(self) -> Optional[Money]:
        active = [c for c in self._ticket_categories if c.is_active]
        if not active:
            return None
        return min(active, key=lambda c: c.price.amount).price

    def _find_category_or_raise(self, category_id: str) -> TicketCategory:
        for c in self._ticket_categories:
            if c.id == category_id:
                return c
        raise ValueError(f"Ticket category {category_id} not found")

    @property
    def ticket_categories(self) -> list[TicketCategory]:
        return list(self._ticket_categories)
