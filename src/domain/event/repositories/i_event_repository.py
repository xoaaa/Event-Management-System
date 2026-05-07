from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.event import Event


class IEventRepository(ABC):

    @abstractmethod
    def save(self, event: Event) -> None:
        """Persist a new or updated Event aggregate."""
        ...

    @abstractmethod
    def find_by_id(self, event_id: UUID) -> Optional[Event]:
        """Return the Event with the given id, or None if not found."""
        ...

    @abstractmethod
    def find_all_published(self) -> List[Event]:
        """Return all Events with status Published."""
        ...