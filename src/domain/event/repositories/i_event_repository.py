from abc import ABC, abstractmethod
from typing import Optional
from src.domain.event.event import Event


class IEventRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Event]: ...

    @abstractmethod
    async def find_all_published(self) -> list[Event]: ...

    @abstractmethod
    async def save(self, event: Event) -> None: ...
