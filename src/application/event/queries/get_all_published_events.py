from dataclasses import dataclass
from typing import List

from domain.event.repositories.i_event_repository import IEventRepository
from application.event.dtos.event_dto import EventDTO


@dataclass
class GetAllPublishedEventsQuery:
    pass


class GetAllPublishedEventsQueryHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, query: GetAllPublishedEventsQuery) -> List[EventDTO]:
        events = self._event_repository.find_all_published()
        return [EventDTO.from_domain(event) for event in events]