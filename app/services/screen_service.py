import uuid

from sqlalchemy.orm import Session

from app.db.models import Screen, Theater
from app.schemas.screen import ScreenCreate


def create_screen(db: Session, screen_data: ScreenCreate) -> Screen | None:
    theater_exists = db.query(Theater).filter(Theater.id == screen_data.theater_id).first()
    if theater_exists is None:
        return None

    new_screen = Screen(
        theater_id=screen_data.theater_id,
        name=screen_data.name,
    )
    db.add(new_screen)
    db.commit()
    db.refresh(new_screen)
    return new_screen


def get_all_screens(db: Session) -> list[Screen]:
    return db.query(Screen).all()


def get_screen_by_id(db: Session, screen_id: uuid.UUID) -> Screen | None:
    return db.query(Screen).filter(Screen.id == screen_id).first()