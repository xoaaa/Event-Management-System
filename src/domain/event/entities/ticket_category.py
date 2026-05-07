from enum import Enum
from src.domain.shared.value_objects.money import Money
from src.domain.shared.value_objects.date_range import DateRange


class TicketCategoryStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class TicketCategory:
    def __init__(
        self,
        id: str,
        event_id: str,
        name: str,
        price: Money,
        quota: int,
        sales_period: DateRange,
        reserved_quota: int = 0,
        status: TicketCategoryStatus = TicketCategoryStatus.ACTIVE,
    ):
        if price.amount < 0:
            raise ValueError("Ticket price cannot be negative")
        if quota <= 0:
            raise ValueError("Ticket quota must be greater than zero")

        self.id = id
        self.event_id = event_id
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_period = sales_period
        self.reserved_quota = reserved_quota
        self.status = status

    @property
    def remaining_quota(self) -> int:
        return self.quota - self.reserved_quota

    @property
    def is_active(self) -> bool:
        return self.status == TicketCategoryStatus.ACTIVE

    def disable(self) -> None:
        self.status = TicketCategoryStatus.INACTIVE

    def reserve_quota(self, quantity: int) -> None:
        if not self.is_active:
            raise ValueError("Ticket category is not active")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if self.remaining_quota < quantity:
            raise ValueError("Insufficient ticket quota")
        self.reserved_quota += quantity

    def release_quota(self, quantity: int) -> None:
        self.reserved_quota = max(0, self.reserved_quota - quantity)
