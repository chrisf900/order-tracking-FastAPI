from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductEntity:
    id: str
    uuid: str
    unit: float
    price: float
    name: str
    sku: str | None = None
    brand_uuid: str | None = None
    description: str | None = None
    unit_size: float | None = None
    weight: float | None = None
    category_uuid: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ProductForPricingEntity:
    id: int
    sku: str
    unit: float
    price: float
