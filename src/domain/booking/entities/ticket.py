from uuid import UUID

from ...shared.value_objects.ticket_code import TicketCode
from .ticket_status import TicketStatus


class Ticket:
    def __init__(
        self,
        id: UUID,
        booking_id: UUID,
        ticket_category_id: UUID,
        ticket_code: TicketCode,
    ) -> None:
        self._id = id
        self._booking_id = booking_id
        self._ticket_category_id = ticket_category_id
        self._ticket_code = ticket_code
        self._status: TicketStatus = TicketStatus.ACTIVE

    def check_in(self) -> None:
        if self._status == TicketStatus.CHECKED_IN:
            raise ValueError("Ticket has already been checked in.")
        self._status = TicketStatus.CHECKED_IN

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def booking_id(self) -> UUID:
        return self._booking_id

    @property
    def ticket_category_id(self) -> UUID:
        return self._ticket_category_id

    @property
    def ticket_code(self) -> TicketCode:
        return self._ticket_code

    @property
    def status(self) -> TicketStatus:
        return self._status

    @property
    def is_checked_in(self) -> bool:
        return self._status == TicketStatus.CHECKED_IN