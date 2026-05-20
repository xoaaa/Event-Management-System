from abc import ABC, abstractmethod
from application.ticket.commands.check_in_ticket import CheckInTicketCommand


class ITicketApplicationService(ABC):

    @abstractmethod
    def check_in_ticket(self, command: CheckInTicketCommand) -> None:
        """Check in a ticket on a paid booking."""
        ...