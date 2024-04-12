# Orders Service Models
from src.config.db import Base
from src.infra.db.models.order import Order
from src.infra.db.models.order_detail import OrderDetail

__all__ = ["Base", "Order", "OrderDetail"]