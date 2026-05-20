from dataclasses import dataclass
from uuid import UUID

from domain.event.repositories.i_event_repository import IEventRepository


@dataclass
class PublishEventCommand:
    event_id: UUID


class PublishEventCommandHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, command: PublishEventCommand) -> None:
        event = self._event_repository.find_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event '{command.event_id}' not found.")
        event.publish()
        self._event_repository.save(event)