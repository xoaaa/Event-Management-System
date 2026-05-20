from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from application.refund.commands.request_refund import RequestRefundCommand
from application.refund.commands.approve_refund import ApproveRefundCommand
from application.refund.commands.reject_refund import RejectRefundCommand
from application.refund.commands.mark_refund_as_paid_out import MarkRefundAsPaidOutCommand
from application.refund.queries.get_refund_by_id import GetRefundByIdQuery
from application.refund.dtos.refund_dto import RefundDTO


class IRefundApplicationService(ABC):

    @abstractmethod
    def request_refund(self, command: RequestRefundCommand) -> UUID:
        """Request a refund for a ticket and return the refund ID."""
        ...

    @abstractmethod
    def approve_refund(self, command: ApproveRefundCommand) -> None:
        """Approve a requested refund."""
        ...

    @abstractmethod
    def reject_refund(self, command: RejectRefundCommand) -> None:
        """Reject a requested refund with a reason."""
        ...

    @abstractmethod
    def mark_refund_as_paid_out(self, command: MarkRefundAsPaidOutCommand) -> None:
        """Mark an approved refund as paid out."""
        ...

    @abstractmethod
    def get_refund_by_id(self, query: GetRefundByIdQuery) -> Optional[RefundDTO]:
        """Return a RefundDTO by ID, or None if not found."""
        ...