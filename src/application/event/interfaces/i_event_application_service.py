from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from application.event.commands.create_event import CreateEventCommand
from application.event.commands.publish_event import PublishEventCommand
from application.event.commands.cancel_event import CancelEventCommand
from application.event.commands.add_ticket_category import AddTicketCategoryCommand
from application.event.commands.disable_ticket_category import DisableTicketCategoryCommand
from application.event.queries.get_event_by_id import GetEventByIdQuery
from application.event.queries.get_all_published_events import GetAllPublishedEventsQuery
from application.event.dtos.event_dto import EventDTO


class IEventApplicationService(ABC):

    @abstractmethod
    def create_event(self, command: CreateEventCommand) -> UUID:
        """Create a new event and return its ID."""
        ...

    @abstractmethod
    def publish_event(self, command: PublishEventCommand) -> None:
        """Publish a draft event."""
        ...

    @abstractmethod
    def cancel_event(self, command: CancelEventCommand) -> None:
        """Cancel a published event."""
        ...

    @abstractmethod
    def add_ticket_category(self, command: AddTicketCategoryCommand) -> UUID:
        """Add a ticket category to an event and return its ID."""
        ...

    @abstractmethod
    def disable_ticket_category(self, command: DisableTicketCategoryCommand) -> None:
        """Disable a ticket category on an event."""
        ...

    @abstractmethod
    def get_event_by_id(self, query: GetEventByIdQuery) -> Optional[EventDTO]:
        """Return an EventDTO by ID, or None if not found."""
        ...

    @abstractmethod
    def get_all_published_events(self, query: GetAllPublishedEventsQuery) -> List[EventDTO]:
        """Return all published events as DTOs."""
        ...