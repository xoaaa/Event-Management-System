from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from domain.event.entities.ticket_category import TicketCategory
from domain.event.entities.event import Event


@dataclass
class TicketCategoryDTO:
    id: UUID
    event_id: UUID
    name: str
    price_amount: Decimal
    price_currency: str
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime
    is_active: bool

    @staticmethod
    def from_domain(tc: TicketCategory) -> "TicketCategoryDTO":
        return TicketCategoryDTO(
            id=tc.id,
            event_id=tc.event_id,
            name=tc.name,
            price_amount=tc.price.amount,
            price_currency=tc.price.currency,
            quota=tc.quota,
            sales_start_date=tc.sales_start_date,
            sales_end_date=tc.sales_end_date,
            is_active=tc.is_active,
        )


@dataclass
class EventDTO:
    id: UUID
    organizer_id: UUID
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    max_capacity: int
    status: str
    ticket_categories: List[TicketCategoryDTO]

    @staticmethod
    def from_domain(event: Event) -> "EventDTO":
        return EventDTO(
            id=event.id,
            organizer_id=event.organizer_id,
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            max_capacity=event.max_capacity,
            status=event.status.value,
            ticket_categories=[
                TicketCategoryDTO.from_domain(tc)
                for tc in event.ticket_categories
            ],
        )