import uuid

from pydantic import BaseModel


class ScreenCreate(BaseModel):
    theater_id: uuid.UUID
    name: str


class ScreenResponse(BaseModel):
    id: uuid.UUID
    theater_id: uuid.UUID
    name: str

    model_config = {"from_attributes": True}