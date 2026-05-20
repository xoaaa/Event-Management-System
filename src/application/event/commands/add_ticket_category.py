from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from domain.event.repositories.i_event_repository import IEventRepository
from domain.shared.value_objects.money import Money


@dataclass
class AddTicketCategoryCommand:
    event_id: UUID
    name: str
    price_amount: Decimal
    price_currency: str
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime


class AddTicketCategoryCommandHandler:
    def __init__(self, event_repository: IEventRepository) -> None:
        self._event_repository = event_repository

    def handle(self, command: AddTicketCategoryCommand) -> UUID:
        event = self._event_repository.find_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event '{command.event_id}' not found.")
        category = event.add_ticket_category(
            name=command.name,
            price=Money(command.price_amount, command.price_currency),
            quota=command.quota,
            sales_start_date=command.sales_start_date,
            sales_end_date=command.sales_end_date,
        )
        self._event_repository.save(event)
        return category.id