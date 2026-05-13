from abc import ABC
from datetime import datetime, timezone
from uuid import UUID, uuid4


class DomainEvent(ABC):
    def __init__(self) -> None:
        self.id: UUID = uuid4()
        self.occurred_on: datetime = datetime.now(timezone.utc)