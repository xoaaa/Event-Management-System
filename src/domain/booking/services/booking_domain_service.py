import uuid
from datetime import datetime
from uuid import UUID

from ...event.entities.event import Event
from ...event.entities.event_status import EventStatus
from ...shared.value_objects.money import Money
from ..entities.booking import Booking


class BookingDomainService:
    """
    Domain service responsible for creating a Booking.

    This logic does not belong inside the Booking aggregate (it has no
    knowledge of Event) nor inside the Event aggregate (it should not
    create Bookings). The coordination between the two aggregates is
    therefore placed here.
    """

    def create_booking(
        self,
        event: Event,
        ticket_category_id: UUID,
        booker_id: UUID,
        quantity: int,
        payment_deadline: datetime,
    ) -> Booking:
        if event.status != EventStatus.PUBLISHED:
            raise ValueError(
                "Bookings can only be made for events that are Published."
            )

        category = next(
            (tc for tc in event.ticket_categories if tc.id == ticket_category_id),
            None,
        )
        if category is None:
            raise ValueError(
                f"Ticket category '{ticket_category_id}' does not exist on this event."
            )
        if not category.is_active:
            raise ValueError(
                "Bookings cannot be made for a disabled ticket category."
            )

        return Booking(
            id=uuid.uuid4(),
            event_id=event.id,
            ticket_category_id=category.id,
            booker_id=booker_id,
            quantity=quantity,
            unit_price=category.price,
            payment_deadline=payment_deadline,
        )