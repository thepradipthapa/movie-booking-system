import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ShowCreate(BaseModel):
    movie_id: uuid.UUID
    screen_id: uuid.UUID
    start_time: datetime
    base_price: Decimal


class ShowResponse(BaseModel):
    id: uuid.UUID
    movie_id: uuid.UUID
    screen_id: uuid.UUID
    start_time: datetime
    base_price: Decimal

    model_config = {"from_attributes": True}