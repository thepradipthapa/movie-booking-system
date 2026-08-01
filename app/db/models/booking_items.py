import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BookingItem(Base):
    __tablename__ = "booking_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False
    )
    show_seat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("show_seats.id"), unique=True, nullable=False
    )