import uuid

from sqlalchemy.orm import Session

from app.db.models import Theater
from app.schemas.theater import TheaterCreate


def create_theater(db: Session, theater_data: TheaterCreate) -> Theater:
    new_theater = Theater(
        name=theater_data.name,
        city=theater_data.city,
    )
    db.add(new_theater)
    db.commit()
    db.refresh(new_theater)
    return new_theater


def get_all_theaters(db: Session) -> list[Theater]:
    return db.query(Theater).all()


def get_theater_by_id(db: Session, theater_id: uuid.UUID) -> Theater | None:
    return db.query(Theater).filter(Theater.id == theater_id).first()
