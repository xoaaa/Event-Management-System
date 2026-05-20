from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.booking.services.booking_domain_service import BookingDomainService
from domain.booking.repositories.i_booking_repository import IBookingRepository
from domain.event.repositories.i_event_repository import IEventRepository


@dataclass
class CreateBookingCommand:
    event_id: UUID
    ticket_category_id: UUID
    booker_id: UUID
    quantity: int
    payment_deadline: datetime

class CreateBookingCommandHandler:
    def _init_(
        self,
        event_repository: IEventRepository,
        booking_repository: IBookingRepository,
        booking_domain_service: BookingDomainService,
    ) -> None:
        self._event_repository = event_repository
        self._booking_repository = booking_repository
        self._booking_domain_service = booking_domain_service

    def handle(self, command: CreateBookingCommand) -> UUID:
        event = self._event_repository.find_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event '{command.event_id}' not found.")
        booking = self._booking_domain_service.create_booking(
            event=event,ticket_category_id=command.ticket_category_id,
            booker_id=command.booker_id,
            quantity=command.quantity,
            payment_deadline=command.payment_deadline,
        )
        self._booking_repository.save(booking)
        return booking.id