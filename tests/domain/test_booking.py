import uuid
import pytest
from decimal import Decimal
from datetime import datetime

from domain.booking.entities.booking import Booking
from domain.booking.entities.booking_status import BookingStatus
from domain.booking.entities.ticket_status import TicketStatus
from domain.shared.value_objects.money import Money

from .conftest import UNIT_PRICE, TOTAL_2, DEADLINE


class TestBookingCreation:
    def test_booking_cannot_be_created_with_zero_quantity(self):
        with pytest.raises(ValueError, match="quantity"):
            Booking(
                id=uuid.uuid4(),
                event_id=uuid.uuid4(),
                ticket_category_id=uuid.uuid4(),
                booker_id=uuid.uuid4(),
                quantity=0,
                unit_price=UNIT_PRICE,
                payment_deadline=DEADLINE,
            )

    def test_booking_cannot_be_created_with_negative_quantity(self):
        with pytest.raises(ValueError, match="quantity"):
            Booking(
                id=uuid.uuid4(),
                event_id=uuid.uuid4(),
                ticket_category_id=uuid.uuid4(),
                booker_id=uuid.uuid4(),
                quantity=-1,
                unit_price=UNIT_PRICE,
                payment_deadline=DEADLINE,
            )

    def test_booking_total_price_is_unit_price_multiplied_by_quantity(
        self, pending_booking
    ):
        assert pending_booking.total_price == TOTAL_2

    def test_booking_is_created_with_pending_payment_status(self, pending_booking):
        assert pending_booking.status == BookingStatus.PENDING_PAYMENT


class TestBookingPayment:
    def test_booking_cannot_be_paid_after_payment_deadline(self, pending_booking):
        with pytest.raises(ValueError, match="deadline"):
            pending_booking.pay(TOTAL_2, paid_at=datetime(2025, 5, 21))

    def test_booking_cannot_be_paid_with_incorrect_payment_amount(self, pending_booking):
        wrong_amount = Money(Decimal("100000"), "IDR")
        with pytest.raises(ValueError, match="amount"):
            pending_booking.pay(wrong_amount, paid_at=datetime(2025, 5, 19))

    def test_booking_can_be_paid_with_correct_amount_before_deadline(
        self, pending_booking
    ):
        pending_booking.pay(TOTAL_2, paid_at=datetime(2025, 5, 19))
        assert pending_booking.status == BookingStatus.PAID

    def test_booking_generates_tickets_equal_to_quantity_on_payment(
        self, pending_booking
    ):
        pending_booking.pay(TOTAL_2, paid_at=datetime(2025, 5, 19))
        assert len(pending_booking.tickets) == 2


class TestBookingExpiry:
    def test_paid_booking_cannot_expire(self, paid_booking):
        with pytest.raises(ValueError, match="paid"):
            paid_booking.expire()

    def test_pending_booking_can_expire(self, pending_booking):
        pending_booking.expire()
        assert pending_booking.status == BookingStatus.EXPIRED


class TestTicketCheckIn:
    def test_checked_in_ticket_cannot_be_checked_in_again(self, paid_booking):
        ticket = paid_booking.tickets[0]
        paid_booking.check_in_ticket(ticket.id)

        with pytest.raises(ValueError, match="already been checked in"):
            paid_booking.check_in_ticket(ticket.id)

    def test_ticket_status_changes_to_checked_in(self, paid_booking):
        ticket = paid_booking.tickets[0]
        assert ticket.status == TicketStatus.ACTIVE

        paid_booking.check_in_ticket(ticket.id)
        assert ticket.status == TicketStatus.CHECKED_IN
        assert ticket.is_checked_in is True
