from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DateRange:
    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date")

    def contains(self, date: datetime) -> bool:
        return self.start_date <= date <= self.end_date

    def is_ended_before(self, date: datetime) -> bool:
        return self.end_date <= date
