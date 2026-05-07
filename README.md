# Event Ticketing & Booking System

EF234402 - Software Construction
Institut Teknologi Sepuluh Nopember

## Tech Stack
- Language : Python 3.12
- Framework: FastAPI
- Database : PostgreSQL
- Architecture: Clean Architecture + Domain-Driven Design

## How to Run
pip install -r requirements.txt
uvicorn src.presentation.http.main:app --reload

## How to Run Tests
pytest tests/

## Folder Structure
src/
  domain/         - Aggregates, entities, value objects, domain events, repository interfaces
  application/    - Commands, queries, handlers, DTOs, application service interfaces
  infrastructure/ - PostgreSQL repositories, external service implementations
  presentation/   - FastAPI routers and controllers

docs/
  business-rules.md
  domain-model-draft.md
  ubiquitous-language.md
