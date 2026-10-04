import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateSeatError, ScreenNotFoundError
from app.core.security import get_current_user
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.seat import SeatCreate, SeatResponse
from app.services import seat_service

router = APIRouter(prefix="/seats", tags=["seats"])


@router.post("/", response_model=SeatResponse, status_code=201)
def create_seat(
    seat_data: SeatCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    try:
        return seat_service.create_seat(db, seat_data)
    except ScreenNotFoundError:
        raise HTTPException(status_code=404, detail="Screen not found")
    except DuplicateSeatError:
        raise HTTPException(status_code=409, detail="Seat already exists on this screen")


@router.get("/", response_model=list[SeatResponse])
def list_seats(db: Session = Depends(get_db)):
    return seat_service.get_all_seats(db)


@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: uuid.UUID, db: Session = Depends(get_db)):
    seat = seat_service.get_seat_by_id(db, seat_id)
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat