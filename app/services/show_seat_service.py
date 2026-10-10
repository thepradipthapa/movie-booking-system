from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import SeatNotAvailableError, ShowSeatNotFoundError
from app.db.models.show_seat import ShowSeat
from app.db.models.user import User


def hold_seat(db: Session, show_id: UUID, seat_id: UUID, user: User) -> ShowSeat:
    show_seat = (
        db.query(ShowSeat)
        .filter(ShowSeat.show_id == show_id, ShowSeat.seat_id == seat_id)
        .first()
    )
    if show_seat is None:
        raise ShowSeatNotFoundError()

    now = datetime.now(UTC)

    if show_seat.status == "BOOKED":
        raise SeatNotAvailableError()

    if show_seat.status == "HELD" and show_seat.hold_expires_at > now:
        # Hold is still valid
        if show_seat.held_by_user_id == user.id:
            return show_seat  # idempotent: don't extend, don't change
        raise SeatNotAvailableError()

    # AVAILABLE, or HELD but expired (check-on-read): take it
    show_seat.status = "HELD"
    show_seat.held_by_user_id = user.id
    show_seat.hold_expires_at = now + timedelta(minutes=settings.HOLD_DURATION_MINUTES)

    db.commit()
    db.refresh(show_seat)
    return show_seat
