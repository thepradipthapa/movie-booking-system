import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.movie import MovieCreate, MovieResponse
from app.services import movie_service

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=MovieResponse, status_code=201)
def create_movie(movie_data: MovieCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(db, movie_data)


@router.get("/", response_model=list[MovieResponse])
def list_movies(db: Session = Depends(get_db)):
    return movie_service.get_all_movies(db)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: uuid.UUID, db: Session = Depends(get_db)):
    movie = movie_service.get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie