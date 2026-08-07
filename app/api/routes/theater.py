import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.theater import TheaterCreate, TheaterResponse
from app.services import theater_service

router = APIRouter(prefix="/theaters", tags=["theaters"])


@router.post("/", response_model=TheaterResponse, status_code=201)
def create_theater(theater_data: TheaterCreate, db: Session = Depends(get_db)):
    return theater_service.create_theater(db, theater_data)


@router.get("/", response_model=list[TheaterResponse])
def list_theaters(db: Session = Depends(get_db)):
    return theater_service.get_all_theaters(db)


@router.get("/{theater_id}", response_model=TheaterResponse)
def get_theater(theater_id: uuid.UUID, db: Session = Depends(get_db)):
    theater = theater_service.get_theater_by_id(db, theater_id)
    if theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater