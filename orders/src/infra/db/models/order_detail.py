import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from src.config.db import Base


class OrderDetail(Base):
    __tablename__ = "order_detail"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    order_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
    product_id: Mapped[int] = mapped_column(index=True)
    product_uuid: Mapped[str] = mapped_column(index=True, unique=True)
    quantity: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
