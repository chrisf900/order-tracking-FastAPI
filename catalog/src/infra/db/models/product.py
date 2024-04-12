import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.config.db import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    brand_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("brand.uuid"), index=True
    )
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    unit: Mapped[float] = mapped_column(Float, nullable=True)
    unit_size: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    category_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.uuid"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )

    brand = relationship("Brand")
    category = relationship("Category")
