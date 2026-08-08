import uuid

from sqlalchemy.orm import Session

from app.db.models import Movie
from app.schemas.movie import MovieCreate


def create_movie(db: Session, movie_data: MovieCreate) -> Movie:
    new_movie = Movie(
        title=movie_data.title,
        duration_minutes=movie_data.duration_minutes,
        language=movie_data.language,
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def get_all_movies(db: Session) -> list[Movie]:
    return db.query(Movie).all()


def get_movie_by_id(db: Session, movie_id: uuid.UUID) -> Movie | None:
    return db.query(Movie).filter(Movie.id == movie_id).first()