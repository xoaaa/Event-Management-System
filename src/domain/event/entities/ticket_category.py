from datetime import datetime
from uuid import UUID

from ...shared.value_objects.money import Money


class TicketCategory:
    def __init__(
        self,
        id: UUID,
        event_id: UUID,
        name: str,
        price: Money,
        quota: int,
        sales_start_date: datetime,
        sales_end_date: datetime,
    ) -> None:
        if not name or not name.strip():
            raise ValueError("Ticket category name cannot be empty.")
        if quota <= 0:
            raise ValueError("Ticket category quota must be greater than zero.")
        if sales_end_date < sales_start_date:
            raise ValueError("Sales end date cannot be earlier than sales start date.")

        self._id = id
        self._event_id = event_id
        self._name = name
        self._price = price
        self._quota = quota
        self._sales_start_date = sales_start_date
        self._sales_end_date = sales_end_date
        self._is_active: bool = True

    def disable(self) -> None:
        self._is_active = False

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def event_id(self) -> UUID:
        return self._event_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Money:
        return self._price

    @property
    def quota(self) -> int:
        return self._quota

    @property
    def sales_start_date(self) -> datetime:
        return self._sales_start_date

    @property
    def sales_end_date(self) -> datetime:
        return self._sales_end_date

    @property
    def is_active(self) -> bool:
        return self._is_active