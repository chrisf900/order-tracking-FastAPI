import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from src.config.db import Base


class Order(Base):
    __tablename__ = "order"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    user_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
    delivery_status: Mapped[str] = mapped_column(
        String(30), default="DRAFT", index=True
    )
    total_amount: Mapped[float] = mapped_column(Float, nullable=True, default=float(0))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
