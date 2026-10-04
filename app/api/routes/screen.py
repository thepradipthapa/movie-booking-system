import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.screen import ScreenCreate, ScreenResponse
from app.services import screen_service

router = APIRouter(prefix="/screens", tags=["screens"])


@router.post("/", response_model=ScreenResponse, status_code=201)
def create_screen(
    screen_data: ScreenCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    screen = screen_service.create_screen(db, screen_data)
    if screen is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return screen


@router.get("/", response_model=list[ScreenResponse])
def list_screens(db: Session = Depends(get_db)):
    return screen_service.get_all_screens(db)


@router.get("/{screen_id}", response_model=ScreenResponse)
def get_screen(screen_id: uuid.UUID, db: Session = Depends(get_db)):
    screen = screen_service.get_screen_by_id(db, screen_id)
    if screen is None:
        raise HTTPException(status_code=404, detail="Screen not found")
    return screen