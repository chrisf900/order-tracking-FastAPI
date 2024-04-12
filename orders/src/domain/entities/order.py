from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderEntity:
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OrderStatusUpdateEntity:
    uuid: str
    old_status: str
    new_status: str
    updated_at: Optional[datetime] = None
