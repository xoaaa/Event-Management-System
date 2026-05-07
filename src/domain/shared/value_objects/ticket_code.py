from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class TicketCode:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Ticket code cannot be empty")

    @classmethod
    def generate(cls) -> "TicketCode":
        return cls(value=str(uuid4()).replace("-", "").upper())
