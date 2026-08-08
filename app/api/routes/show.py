import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateShowError,
    MovieNotFoundError,
    ScreenNotFoundError,
)
from app.db.base import get_db
from app.schemas.show import ShowCreate, ShowResponse
from app.services import show_service

router = APIRouter(prefix="/shows", tags=["shows"])


@router.post("/", response_model=ShowResponse, status_code=201)
def create_show(show_data: ShowCreate, db: Session = Depends(get_db)):
    try:
        return show_service.create_show(db, show_data)
    except MovieNotFoundError:
        raise HTTPException(status_code=404, detail="Movie not found")
    except ScreenNotFoundError:
        raise HTTPException(status_code=404, detail="Screen not found")
    except DuplicateShowError:
        raise HTTPException(status_code=409, detail="A show already exists on this screen at this time")


@router.get("/", response_model=list[ShowResponse])
def list_shows(db: Session = Depends(get_db)):
    return show_service.get_all_shows(db)


@router.get("/{show_id}", response_model=ShowResponse)
def get_show(show_id: uuid.UUID, db: Session = Depends(get_db)):
    show = show_service.get_show_by_id(db, show_id)
    if show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return show