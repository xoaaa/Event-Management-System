from dataclasses import dataclass
from src.domain.shared.interfaces.aggregate_root import DomainEvent


@dataclass
class TicketReserved(DomainEvent):
    booking_id: str = ""


@dataclass
class BookingPaid(DomainEvent):
    booking_id: str = ""


@dataclass
class BookingExpired(DomainEvent):
    booking_id: str = ""
