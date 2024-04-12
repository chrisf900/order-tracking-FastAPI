from datetime import datetime
from typing import List

from pydantic import BaseModel
from src.application.dtos.catalog_dto import OrderProductDTO


class OrderDTO(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ItemDTO(BaseModel):
    uuid: str
    product_id: int
    quantity: float


class OrderDetailDTO(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    items: List[ItemDTO]
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OrderWithProductsDTO(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    items: List[OrderProductDTO]
    created_at: datetime | None = None
    updated_at: datetime | None = None
