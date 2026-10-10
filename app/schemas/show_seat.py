from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HoldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    show_id: UUID
    seat_id: UUID
    status: str
    hold_expires_at: datetime | None