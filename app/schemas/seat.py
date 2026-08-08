import uuid

from pydantic import BaseModel


class SeatCreate(BaseModel):
    screen_id: uuid.UUID
    row_label: str
    seat_number: int
    seat_type: str = "standard"


class SeatResponse(BaseModel):
    id: uuid.UUID
    screen_id: uuid.UUID
    row_label: str
    seat_number: int
    seat_type: str

    model_config = {"from_attributes": True}