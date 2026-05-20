from dataclasses import dataclass
from uuid import UUID

from domain.refund.repositories.i_refund_repository import IRefundRepository


@dataclass
class ApproveRefundCommand:
    refund_id: UUID


class ApproveRefundCommandHandler:
    def _init_(self, refund_repository: IRefundRepository) -> None:
        self._refund_repository = refund_repository

    def handle(self, command: ApproveRefundCommand) -> None:
        refund = self._refund_repository.find_by_id(command.refund_id)
        if refund is None:
            raise ValueError(f"Refund '{command.refund_id}' not found.")
        refund.approve()
        self._refund_repository.save(refund)
