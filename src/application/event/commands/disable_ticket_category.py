from dataclasses import dataclass
from uuid import UUID

from domain.event.repositories.i_event_repository import IEventRepository


@dataclass
class DisableTicketCategoryCommand:
    event_id: UUID
    ticket_category_id: UUID


class DisableTicketCategoryCommandHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, command: DisableTicketCategoryCommand) -> None:
        event = self._event_repository.find_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event '{command.event_id}' not found.")
        event.disable_ticket_category(command.ticket_category_id)
        self._event_repository.save(event)