import uuid
import pytest
from decimal import Decimal
from datetime import datetime

from domain.event.entities.event import Event
from domain.event.entities.event_status import EventStatus
from domain.shared.value_objects.money import Money

from .conftest import UNIT_PRICE, SALES_START, SALES_END


class TestEventCreation:
    def test_event_cannot_be_created_with_end_date_before_start_date(self, organizer_id):
        with pytest.raises(ValueError, match="end date"):
            Event(
                id=uuid.uuid4(),
                organizer_id=organizer_id,
                name="Bad Event",
                description="",
                start_date=datetime(2025, 6, 2),
                end_date=datetime(2025, 6, 1),
                location="Jakarta",
                max_capacity=100,
            )

    def test_event_cannot_be_created_with_zero_capacity(self, organizer_id):
        with pytest.raises(ValueError, match="capacity"):
            Event(
                id=uuid.uuid4(),
                organizer_id=organizer_id,
                name="Bad Event",
                description="",
                start_date=datetime(2025, 6, 1),
                end_date=datetime(2025, 6, 2),
                location="Jakarta",
                max_capacity=0,
            )

    def test_event_cannot_be_created_with_negative_capacity(self, organizer_id):
        with pytest.raises(ValueError, match="capacity"):
            Event(
                id=uuid.uuid4(),
                organizer_id=organizer_id,
                name="Bad Event",
                description="",
                start_date=datetime(2025, 6, 1),
                end_date=datetime(2025, 6, 2),
                location="Jakarta",
                max_capacity=-10,
            )

    def test_event_is_created_with_draft_status(self, draft_event):
        assert draft_event.status == EventStatus.DRAFT


class TestEventPublish:
    def test_event_cannot_be_published_without_active_ticket_category(self, draft_event):
        with pytest.raises(ValueError, match="ticket category"):
            draft_event.publish()

    def test_event_cannot_be_published_without_active_ticket_category_when_all_disabled(
        self, draft_event
    ):
        cat = draft_event.add_ticket_category(
            name="Regular",
            price=UNIT_PRICE,
            quota=50,
            sales_start_date=SALES_START,
            sales_end_date=SALES_END,
        )
        draft_event.disable_ticket_category(cat.id)
        draft_event.pull_domain_events()

        with pytest.raises(ValueError, match="ticket category"):
            draft_event.publish()

    def test_event_can_be_published_with_active_ticket_category(
        self, draft_event_with_category
    ):
        draft_event_with_category.publish()
        assert draft_event_with_category.status == EventStatus.PUBLISHED

    def test_ticket_category_quota_cannot_exceed_event_capacity(self, draft_event):
        with pytest.raises(ValueError, match="capacity"):
            draft_event.add_ticket_category(
                name="VIP",
                price=UNIT_PRICE,
                quota=200,              # max_capacity is 100
                sales_start_date=SALES_START,
                sales_end_date=SALES_END,
            )


class TestEventCancel:
    def test_only_published_event_can_be_cancelled(self, draft_event_with_category):
        draft_event_with_category.publish()
        draft_event_with_category.pull_domain_events()

        draft_event_with_category.cancel()
        assert draft_event_with_category.status == EventStatus.CANCELLED

    def test_draft_event_cannot_be_cancelled(self, draft_event):
        with pytest.raises(ValueError):
            draft_event.cancel()
