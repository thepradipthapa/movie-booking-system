import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateShowError,
    MovieNotFoundError,
    ScreenNotFoundError,
)
from app.db.models import Movie, Screen, Seat, Show, ShowSeat
from app.schemas.show import ShowCreate


def create_show(db: Session, show_data: ShowCreate) -> Show:
    movie_exists = db.query(Movie).filter(Movie.id == show_data.movie_id).first()
    if movie_exists is None:
        raise MovieNotFoundError()

    screen_exists = db.query(Screen).filter(Screen.id == show_data.screen_id).first()
    if screen_exists is None:
        raise ScreenNotFoundError()

    duplicate = (
        db.query(Show)
        .filter(
            Show.screen_id == show_data.screen_id,
            Show.start_time == show_data.start_time,
        )
        .first()
    )
    if duplicate is not None:
        raise DuplicateShowError()

    new_show = Show(
        movie_id=show_data.movie_id,
        screen_id=show_data.screen_id,
        start_time=show_data.start_time,
        base_price=show_data.base_price,
    )
    db.add(new_show)
    db.flush()  # Flush to get the new_show.id before committing
    
    seats = db.query(Seat).filter(Seat.screen_id == new_show.screen_id).all()
    db.add_all(
        [
            ShowSeat(show_id=new_show.id, seat_id=seat.id, status="AVAILABLE")
            for seat in seats
        ]
    )
    db.commit() # Commit the transaction to save both the new show and its associated seats
    db.refresh(new_show)
    return new_show


def get_all_shows(db: Session) -> list[Show]:
    return db.query(Show).all()


def get_show_by_id(db: Session, show_id: uuid.UUID) -> Show | None:
    return db.query(Show).filter(Show.id == show_id).first()