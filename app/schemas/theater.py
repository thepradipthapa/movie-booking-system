import uuid

from pydantic import BaseModel


class TheaterCreate(BaseModel):
    name: str
    city: str


class TheaterResponse(BaseModel):
    id: uuid.UUID
    name: str
    city: str

    model_config = {"from_attributes": True}