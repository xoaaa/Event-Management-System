from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.event.repositories.i_event_repository import IEventRepository
from application.event.dtos.event_dto import EventDTO


@dataclass
class GetEventByIdQuery:
    event_id: UUID


class GetEventByIdQueryHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, query: GetEventByIdQuery) -> Optional[EventDTO]:
        event = self._event_repository.find_by_id(query.event_id)
        if event is None:
            return None
        return EventDTO.from_domain(event)