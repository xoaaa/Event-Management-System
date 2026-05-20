import uuid
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.event.entities.event import Event
from domain.event.repositories.i_event_repository import IEventRepository


@dataclass
class CreateEventCommand:
    organizer_id: UUID
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    max_capacity: int


class CreateEventCommandHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> UUID:
        event = Event(
            id=uuid.uuid4(),
            organizer_id=command.organizer_id,
            name=command.name,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
            location=command.location,
            max_capacity=command.max_capacity,
        )
        self._event_repository.save(event)
        return event.id