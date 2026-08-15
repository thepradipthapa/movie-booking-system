# Movie Booking System

A production-grade ticket booking backend built with **FastAPI** and **PostgreSQL**.
Focuses on real engineering challenges — concurrent seat reservations, double-booking
prevention, idempotent APIs, and time-based cancellation policies.

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
- Complete CRUD flow of theaters, screens, movies, seats and shows

---
## Engineering Highlights
---
## Tech Stack
 
| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python, FastAPI                     |
| Database    | PostgreSQL                          |
| ORM         | SQLAlchemy 2.0                      |
| Migrations  | Alembic                             |
| Auth        | JWT                                 |
| API Docs    | Swagger UI (auto-generated)         |
 
---
 
## System Requirements
 
### Functional Requirements
 
- User registration and login with JWT-based authentication
- Browse movies, showtimes, and seat maps by city
- Hold seats temporarily during checkout (10-minute TTL)
- Apply coupon codes for percentage or flat discounts
- Confirm booking with payment (mocked)
- Cancel booking only if more than 1 hour before show start
- Admin can create movies, shows, screens, and seats
### Non-Functional Requirements
 
- No two users can ever book the same seat for the same show
- System must remain consistent under concurrent load on the last available seat
- Booking API must be idempotent — safe to retry on network failures
- Hold expiry enforced server-side regardless of client-side timer state
- Security - Passwords hashed with bcrypt — plain text never stored
- Availability
- Performance - smooth and fast booking
- Maintainability - code structure, versioned migrations
- Observability - Structure logging, Request correlations 

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

## High-Level Architecture

---

 ### Booking Request Flow
```
1. GET  /shows/{id}/seats          → fetch current seat availability
2. POST /holds                     → hold selected seats (10-min TTL)
        └── pessimistic lock on ShowSeat row (SELECT FOR UPDATE)
        └── status: AVAILABLE → HELD
3. POST /bookings                  → confirm booking
        └── optimistic lock check (version column)
        └── status: HELD → BOOKED
        └── idempotency key prevents duplicate on retry
4. PATCH /bookings/{id}/cancel     → cancel if > 1hr before show
        └── status: BOOKED → AVAILABLE
```

---

## Database Design

![Entity Relationship Diagram](docs/ERD.png)
---

---

## API Reference

Full interactive docs available at `http://localhost:8000/docs` after running the server.
 
| Method | Endpoint                      | Description                         | Auth     |
|--------|-------------------------------|-------------------------------------|----------|
| GET    | `/movies`                     | List all movies                     | Public   |


--

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

# run server
uv run fastapi dev app/main.py
```


