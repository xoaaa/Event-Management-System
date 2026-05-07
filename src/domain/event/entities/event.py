import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...shared.interfaces.aggregate_root import AggregateRoot
from ...shared.value_objects.money import Money
from .event_status import EventStatus
from .ticket_category import TicketCategory
from ..events.event_created import EventCreated
from ..events.event_published import EventPublished
from ..events.event_cancelled import EventCancelled
from ..events.ticket_category_created import TicketCategoryCreated
from ..events.ticket_category_disabled import TicketCategoryDisabled


class Event(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        organizer_id: UUID,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        location: str,
        max_capacity: int,
    ) -> None:
        super().__init__()

        if not name or not name.strip():
            raise ValueError("Event name cannot be empty.")
        if end_date < start_date:
            raise ValueError("Event end date cannot be earlier than start date.")
        if max_capacity <= 0:
            raise ValueError("Event maximum capacity must be greater than zero.")

        self._id = id
        self._organizer_id = organizer_id
        self._name = name
        self._description = description
        self._start_date = start_date
        self._end_date = end_date
        self._location = location
        self._max_capacity = max_capacity
        self._status: EventStatus = EventStatus.DRAFT
        self._ticket_categories: List[TicketCategory] = []

        self._add_domain_event(EventCreated(
            event_id=self._id,
            organizer_id=self._organizer_id,
            name=self._name,
        ))

    # ------------------------------------------------------------------ #
    #  Commands                                                            #
    # ------------------------------------------------------------------ #

    def publish(self) -> None:
        if self._status != EventStatus.DRAFT:
            raise ValueError("Only a Draft event can be published.")

        active_categories = [tc for tc in self._ticket_categories if tc.is_active]
        if not active_categories:
            raise ValueError(
                "Event must have at least one active ticket category before publishing."
            )

        total_quota = sum(tc.quota for tc in active_categories)
        if total_quota > self._max_capacity:
            raise ValueError(
                "Total ticket category quota exceeds the event maximum capacity."
            )

        self._status = EventStatus.PUBLISHED
        self._add_domain_event(EventPublished(event_id=self._id))

    def cancel(self) -> None:
        if self._status != EventStatus.PUBLISHED:
            raise ValueError("Only a Published event can be cancelled.")

        self._status = EventStatus.CANCELLED
        self._add_domain_event(EventCancelled(event_id=self._id))

    def add_ticket_category(
        self,
        name: str,
        price: Money,
        quota: int,
        sales_start_date: datetime,
        sales_end_date: datetime,
    ) -> TicketCategory:
        if sales_end_date > self._start_date:
            raise ValueError(
                "Ticket sales period must end on or before the event start date."
            )

        active_total = sum(tc.quota for tc in self._ticket_categories if tc.is_active)
        if active_total + quota > self._max_capacity:
            raise ValueError(
                "Adding this ticket category would exceed the event maximum capacity."
            )

        category = TicketCategory(
            id=uuid.uuid4(),
            event_id=self._id,
            name=name,
            price=price,
            quota=quota,
            sales_start_date=sales_start_date,
            sales_end_date=sales_end_date,
        )
        self._ticket_categories.append(category)

        self._add_domain_event(TicketCategoryCreated(
            event_id=self._id,
            ticket_category_id=category.id,
            name=name,
        ))
        return category

    def disable_ticket_category(self, category_id: UUID) -> None:
        if self._status == EventStatus.COMPLETED:
            raise ValueError(
                "Cannot disable a ticket category for a completed event."
            )

        category = self._find_category(category_id)
        if category is None:
            raise ValueError(f"Ticket category '{category_id}' not found.")

        category.disable()
        self._add_domain_event(TicketCategoryDisabled(
            event_id=self._id,
            ticket_category_id=category_id,
        ))

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _find_category(self, category_id: UUID) -> Optional[TicketCategory]:
        for tc in self._ticket_categories:
            if tc.id == category_id:
                return tc
        return None

    # ------------------------------------------------------------------ #
    #  Properties                                                          #
    # ------------------------------------------------------------------ #

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def organizer_id(self) -> UUID:
        return self._organizer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @property
    def location(self) -> str:
        return self._location

    @property
    def max_capacity(self) -> int:
        return self._max_capacity

    @property
    def status(self) -> EventStatus:
        return self._status

    @property
    def ticket_categories(self) -> List[TicketCategory]:
        return list(self._ticket_categories)