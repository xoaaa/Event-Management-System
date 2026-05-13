from enum import Enum


class RefundStatus(Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"