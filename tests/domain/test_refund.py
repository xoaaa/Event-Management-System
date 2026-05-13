import uuid
import pytest
from decimal import Decimal

from domain.refund.refund import Refund
from domain.refund.refund_status import RefundStatus
from domain.shared.value_objects.money import Money

from .conftest import UNIT_PRICE


def make_refund(ticket_is_checked_in: bool = False) -> Refund:
    return Refund(
        id=uuid.uuid4(),
        booking_id=uuid.uuid4(),
        ticket_id=uuid.uuid4(),
        requester_id=uuid.uuid4(),
        amount=UNIT_PRICE,
        ticket_is_checked_in=ticket_is_checked_in,
    )


class TestRefundRequest:
    def test_refund_cannot_be_requested_if_ticket_is_already_checked_in(self):
        with pytest.raises(ValueError, match="checked in"):
            make_refund(ticket_is_checked_in=True)

    def test_refund_is_created_with_requested_status(self):
        refund = make_refund()
        assert refund.status == RefundStatus.REQUESTED


class TestRefundApproval:
    def test_refund_cannot_be_approved_if_not_in_requested_status(self):
        refund = make_refund()
        refund.approve()                # moves to APPROVED

        with pytest.raises(ValueError, match="Requested"):
            refund.approve()            # cannot approve again

    def test_refund_cannot_be_approved_after_rejection(self):
        refund = make_refund()
        refund.reject("Duplicate request.")

        with pytest.raises(ValueError, match="Requested"):
            refund.approve()

    def test_refund_status_changes_to_approved(self):
        refund = make_refund()
        refund.approve()
        assert refund.status == RefundStatus.APPROVED


class TestRefundRejection:
    def test_rejected_refund_must_have_a_rejection_reason(self):
        refund = make_refund()
        with pytest.raises(ValueError, match="[Rr]eason"):
            refund.reject("")

    def test_rejected_refund_cannot_have_whitespace_only_reason(self):
        refund = make_refund()
        with pytest.raises(ValueError, match="[Rr]eason"):
            refund.reject("   ")

    def test_refund_status_changes_to_rejected_with_valid_reason(self):
        refund = make_refund()
        refund.reject("Event was cancelled.")
        assert refund.status == RefundStatus.REJECTED
        assert refund.rejection_reason == "Event was cancelled."


class TestRefundPaidOut:
    def test_refund_can_be_paid_out_after_approval(self):
        refund = make_refund()
        refund.approve()
        refund.mark_as_paid_out()
        assert refund.status == RefundStatus.PAID_OUT

    def test_refund_cannot_be_paid_out_when_still_requested(self):
        refund = make_refund()
        with pytest.raises(ValueError, match="Approved"):
            refund.mark_as_paid_out()
