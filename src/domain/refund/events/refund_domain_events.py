from dataclasses import dataclass
from src.domain.shared.interfaces.aggregate_root import DomainEvent


@dataclass
class RefundRequested(DomainEvent):
    refund_id: str = ""


@dataclass
class RefundApproved(DomainEvent):
    refund_id: str = ""


@dataclass
class RefundRejected(DomainEvent):
    refund_id: str = ""
    reason: str = ""


@dataclass
class RefundPaidOut(DomainEvent):
    refund_id: str = ""
    payment_reference: str = ""
