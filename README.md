# Movie Booking System

A movie booking backend focused on solving real concurrency problems -
preventing double-bookings under race conditions, and enforcing data
integrity at the database level rather than hoping application code never
has a bug.

> **Status: work in progress, built incrementally.**

---


## What's Implemented So Far

- Full relational schema (9 tables) modeling theaters, screens, seats,
  movies, shows, seat-level availability, and bookings
- Data integrity constraints enforced at the database level — including the
  core guarantee that a seat can never be attached to two bookings
- Alembic-managed, version-controlled migrations from the very first table
- Clean project structure separating config, database models, and (soon)
  API routes, request/response schemas, and business logic

*[Roadmap](#roadmap)*

---

## Architecture

```
HTTP Request
    |
    v
FastAPI (routing, request validation via Pydantic)
    |
    v
Service layer (business logic - not yet implemented)
    |
    v
SQLAlchemy (ORM, typed models)
    |
    v
PostgreSQL
```

Alembic sits alongside this, managing how the database schema evolves over
time as a series of version-controlled migration scripts.

**Stack**
- **FastAPI**
- **SQLAlchemy 2.0**
- **Alembic**
- **PostgreSQL**
- **uv**

---

## Key Engineering Decisions

**Why UUIDs instead of auto-increment integers for primary keys?**
Sequential IDs leak information (`/bookings/4582` reveals approximate
volume and lets someone enumerate other users' data) and risk collisions if
this system is ever split into separate services later. Trade-off: worse
index locality than integers — accepted here for the security and
architecture benefit.

**Why a separate `show_seats` table instead of a boolean on `seats`?**
The same physical seat is reused across many showtimes in a day — booked
for a 7PM show, empty for a 2PM show, at the same physical location. A
single boolean on `seats` has nowhere to store three different answers for
three different shows. `show_seats` gives one row per (seat, show)
combination, so availability is tracked per-show, not per-seat.

**How is double-booking actually prevented?**
Via `UNIQUE(show_seat_id)` on the `booking_items` table. A given seat, for
a given show, can physically only ever appear in one booking — enforced by
Postgres itself. Even if application code has a bug and two requests race
to insert a booking for the same seat, the database rejects the second
insert outright. This is the core guarantee the whole schema is built
around.

**Why NUMERIC instead of FLOAT for prices?**
Floats are binary approximations — rounding errors compound across many
transactions until totals stop reconciling. `NUMERIC(10,2)` stores exact
decimal values. Money is never a float, in any system.

**Why TIMESTAMPTZ instead of plain TIMESTAMP?**
`TIMESTAMPTZ` stores the instant in UTC and converts on display. Plain
`TIMESTAMP` has no timezone awareness — if the server and users are ever in
different timezones, showtimes become silently wrong.

**Why does `screens.theater_id` cascade on delete, but `show_seats.seat_id`
doesn't?**
The rule: cascade when the child row is meaningless without its parent;
block when deleting the parent would silently destroy data worth keeping.
A screen cannot exist without its theater, so deleting the theater
correctly cascades. But a single seat can be referenced by `show_seats`
rows across many past shows with real booking history — deleting the seat
should not silently wipe that history, so it's blocked by default instead.

**Why is `held_by_user_id` on `show_seats` nullable?**
Most seats, most of the time, are not being held by anyone — they're just
sitting `AVAILABLE`. Making this column required would mean every seat
needs a fake placeholder user the moment it's created, before anyone has
even opened the seat map. `NULL` correctly represents "genuinely no one is
holding this right now" rather than forcing a meaningless value into
existence.

---

## Database Design

![Entity Relationship Diagram](docs/ERD.png)
---

## Roadmap

- [x] Database schema, models, and migrations
- [ ] Core CRUD APIs (theaters, screens, seats, movies, shows)
- [ ] Authentication (JWT-based)
- [ ] Seat holding mechanism with expiry
- [ ] Booking flow with atomic transactions
- [ ] Concurrency control — pessimistic locking (`SELECT ... FOR UPDATE`)
- [ ] Concurrency control — optimistic locking (version-based), compared
      against pessimistic locking for the same problem
- [ ] Idempotent booking requests (safe retries, no duplicate bookings)
- [ ] Coupon codes
- [ ] Cancellation rules (time-based, before show start)
- [ ] Automated tests, including simulated concurrent booking attempts

---

## Setup

```bash
# clone and enter the project
git clone https://github.com/YOUR_USERNAME/movie-booking-system.git
cd movie-booking-system

# install dependencies
uv sync

# configure environment - create a .env file:
# DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/movie_booking_db
# SECRET_KEY=your-secret-key

# create the database (one-time, manual step)
psql -U postgres -c "CREATE DATABASE movie_booking_db;"

# run migrations
uv run alembic upgrade head
```

## Project Structure

```
app/
├── core/           # settings, config
├── db/
│   ├── base.py     # SQLAlchemy engine/session setup
│   └── models/     # one file per table
├── api/routes/     # FastAPI endpoints (Phase 3)
├── schemas/        # Pydantic request/response models
└── services/       # business logic
alembic/            # version-controlled schema migrations
```

