import uuid

from pydantic import BaseModel


class MovieCreate(BaseModel):
    title: str
    duration_minutes: int
    language: str | None = None


class MovieResponse(BaseModel):
    id: uuid.UUID
    title: str
    duration_minutes: int
    language: str | None

    model_config = {"from_attributes": True}