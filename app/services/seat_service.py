import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateSeatError, ScreenNotFoundError
from app.db.models import Screen, Seat
from app.schemas.seat import SeatCreate


def create_seat(db: Session, seat_data: SeatCreate) -> Seat:
    screen_exists = db.query(Screen).filter(Screen.id == seat_data.screen_id).first()
    if screen_exists is None:
        raise ScreenNotFoundError()

    duplicate = (
        db.query(Seat)
        .filter(
            Seat.screen_id == seat_data.screen_id,
            Seat.row_label == seat_data.row_label,
            Seat.seat_number == seat_data.seat_number,
        )
        .first()
    )
    if duplicate is not None:
        raise DuplicateSeatError()

    new_seat = Seat(
        screen_id=seat_data.screen_id,
        row_label=seat_data.row_label,
        seat_number=seat_data.seat_number,
        seat_type=seat_data.seat_type,
    )
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)
    return new_seat


def get_all_seats(db: Session) -> list[Seat]:
    return db.query(Seat).all()


def get_seat_by_id(db: Session, seat_id: uuid.UUID) -> Seat | None:
    return db.query(Seat).filter(Seat.id == seat_id).first()