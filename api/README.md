# OpenLibrary Books API

This API fetches books from OpenLibrary based on subject and stores them in a PostgreSQL database. It also provides endpoints to list and filter stored books.

## Endpoints
- `/fetch-books` → Fetch and store books by subject
- `/list-books` → List all books
- `/list-books/{subject}` → Filter books by subject
- `/docs` → Swagger UI
- `/` → Healthcheck

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Hosted on Railway