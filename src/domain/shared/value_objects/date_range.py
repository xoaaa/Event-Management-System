from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DateRange:
    start_date: datetime
    end_date: datetime

    def __post_init__(self) -> None:
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date.")

    def contains(self, dt: datetime) -> bool:
        return self.start_date <= dt <= self.end_date

    def is_active(self, now: datetime) -> bool:
        return self.contains(now)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateRange):
            return False
        return self.start_date == other.start_date and self.end_date == other.end_date

    def __repr__(self) -> str:
        return f"DateRange(start={self.start_date!r}, end={self.end_date!r})"