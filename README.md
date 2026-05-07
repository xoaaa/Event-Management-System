# Event Ticketing & Booking System

EF234402 – Software Construction  
Institut Teknologi Sepuluh Nopember

---

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Architecture:** Clean Architecture + Domain-Driven Design

---

## Folder Structure

```
src/
├── domain/                              # Layer 1 — Domain (innermost, no dependencies)
│   ├── shared/
│   │   ├── interfaces/
│   │   │   └── aggregate_root.py        # Base class with domain event tracking
│   │   └── value_objects/
│   │       ├── money.py                 # Value object: amount + currency
│   │       ├── date_range.py            # Value object: start + end date
│   │       └── ticket_code.py           # Value object: unique ticket identifier
│   │
│   ├── event/
│   │   ├── event.py                     # Aggregate Root: Event lifecycle
│   │   ├── entities/
│   │   │   └── ticket_category.py       # Entity: ticket type owned by Event
│   │   ├── events/
│   │   │   └── event_domain_events.py
│   │   └── repositories/
│   │       └── i_event_repository.py    # Abstract repository interface
│   │
│   ├── booking/
│   │   ├── booking.py                   # Aggregate Root: Booking lifecycle
│   │   ├── entities/
│   │   │   └── ticket.py                # Entity: issued ticket owned by Booking
│   │   ├── events/
│   │   │   └── booking_domain_events.py
│   │   └── repositories/
│   │       └── i_booking_repository.py
│   │
│   └── refund/
│       ├── refund.py                    # Aggregate Root: Refund lifecycle
│       ├── events/
│       │   └── refund_domain_events.py
│       └── repositories/
│           └── i_refund_repository.py
│
├── application/                         # Layer 2 — Application (use cases)
│   ├── event/
│   │   ├── commands/                    # CreateEvent, PublishEvent, CancelEvent, etc.
│   │   ├── queries/                     # GetAvailableEvents, GetEventDetails, etc.
│   │   ├── handlers/                    # Command + query handlers
│   │   └── dtos/                        # Input/output data transfer objects
│   ├── booking/
│   │   ├── commands/                    # CreateBooking, PayBooking, ExpireBooking, etc.
│   │   ├── queries/
│   │   ├── handlers/
│   │   └── dtos/
│   ├── ticket/
│   │   ├── commands/                    # CheckInTicket
│   │   ├── queries/                     # GetPurchasedTickets, GetParticipantList, etc.
│   │   ├── handlers/
│   │   └── dtos/
│   ├── refund/
│   │   ├── commands/                    # RequestRefund, ApproveRefund, RejectRefund, etc.
│   │   ├── queries/
│   │   ├── handlers/
│   │   └── dtos/
│   └── shared/
│       └── interfaces/
│           ├── i_payment_gateway.py          # External system interface
│           ├── i_refund_payment_service.py   # External system interface
│           └── i_notification_service.py     # External system interface
│
├── infrastructure/                      # Layer 3 — Infrastructure (DB, external services)
│   ├── database/
│   │   ├── repositories/                # PostgreSQL implementations of repo interfaces
│   │   └── migrations/                  # SQL migration files
│   └── services/
│       ├── payment/                     # i_payment_gateway implementation
│       ├── notification/                # i_notification_service implementation
│       └── refund/                      # i_refund_payment_service implementation
│
└── presentation/                        # Layer 4 — Presentation (FastAPI routers)
    └── http/
        ├── controllers/                 # Business logic delegation (thin layer)
        ├── routers/                     # FastAPI APIRouter definitions per feature
        ├── middleware/                  # Auth, error handling, etc.
        └── dtos/                        # Pydantic request/response models

tests/
└── domain/                              # Unit tests for domain layer

docs/
├── business-rules.md
├── domain-model-draft.md
└── ubiquitous-language.md
```

---

## Dependency Rule

```
Presentation → Application → Domain
Infrastructure → Application (implements interfaces defined in Application)
```

> The Domain layer has **zero** external dependencies — pure Python only.  
> Value objects use `@dataclass(frozen=True)` — immutable by design.  
> Repository interfaces use Python `ABC` (Abstract Base Class) instead of TypeScript interfaces.

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn src.presentation.http.main:app --reload

# Run tests
pytest tests/
```

---

## Docs

- [Business Rules](./docs/business-rules.md)
- [Domain Model Draft](./docs/domain-model-draft.md)
- [Ubiquitous Language Glossary](./docs/ubiquitous-language.md)