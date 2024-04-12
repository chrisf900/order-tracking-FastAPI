from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AddProductToOrderDTO(BaseModel):
    uuid: str
    product_id: int
    quantity: float


class OrderDTO(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrderItemDTO(BaseModel):
    uuid: str
    product_id: int
    quantity: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrderWithItemsDTO(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    items: List[OrderItemDTO]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
