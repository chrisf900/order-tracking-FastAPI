from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderDetailEntity:
    uuid: str
    order_uuid: str
    product_id: int
    quantity: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
