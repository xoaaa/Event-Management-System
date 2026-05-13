import uuid
import pytest
from decimal import Decimal
from datetime import datetime

from domain.event.entities.event import Event
from domain.booking.entities.booking import Booking
from domain.shared.value_objects.money import Money


# ── Shared dates ────────────────────────────────────────────────────────────
EVENT_START = datetime(2025, 6, 1)
EVENT_END   = datetime(2025, 6, 2)
SALES_START = datetime(2025, 5, 1)
SALES_END   = datetime(2025, 5, 31)
DEADLINE    = datetime(2025, 5, 20)

UNIT_PRICE  = Money(Decimal("150000"), "IDR")
TOTAL_2     = Money(Decimal("300000"), "IDR")


# ── Event fixtures ───────────────────────────────────────────────────────────
@pytest.fixture
def organizer_id():
    return uuid.uuid4()


@pytest.fixture
def draft_event(organizer_id):
    event = Event(
        id=uuid.uuid4(),
        organizer_id=organizer_id,
        name="Tech Conference 2025",
        description="Annual tech conference",
        start_date=EVENT_START,
        end_date=EVENT_END,
        location="Jakarta",
        max_capacity=100,
    )
    event.pull_domain_events()   # clear EventCreated
    return event


@pytest.fixture
def draft_event_with_category(draft_event):
    draft_event.add_ticket_category(
        name="Regular",
        price=UNIT_PRICE,
        quota=50,
        sales_start_date=SALES_START,
        sales_end_date=SALES_END,
    )
    draft_event.pull_domain_events()   # clear TicketCategoryCreated
    return draft_event


# ── Booking fixtures ─────────────────────────────────────────────────────────
@pytest.fixture
def pending_booking():
    booking = Booking(
        id=uuid.uuid4(),
        event_id=uuid.uuid4(),
        ticket_category_id=uuid.uuid4(),
        booker_id=uuid.uuid4(),
        quantity=2,
        unit_price=UNIT_PRICE,
        payment_deadline=DEADLINE,
    )
    booking.pull_domain_events()   # clear TicketReserved
    return booking


@pytest.fixture
def paid_booking(pending_booking):
    pending_booking.pay(TOTAL_2, paid_at=datetime(2025, 5, 19))
    pending_booking.pull_domain_events()   # clear BookingPaid
    return pending_booking
