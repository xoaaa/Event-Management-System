from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.refund.repositories.i_refund_repository import IRefundRepository
from application.refund.dtos.refund_dto import RefundDTO


@dataclass
class GetRefundByIdQuery:
    refund_id: UUID


class GetRefundByIdQueryHandler:
    def _init_(self, refund_repository: IRefundRepository) -> None:
        self._refund_repository = refund_repository

    def handle(self, query: GetRefundByIdQuery) -> Optional[RefundDTO]:
        refund = self._refund_repository.find_by_id(query.refund_id)
        if refund is None:
            return None
        return RefundDTO.from_domain(refund)