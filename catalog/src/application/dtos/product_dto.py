from datetime import datetime

from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: int
    uuid: str
    name: str
    sku: str | None
    brand: str | None
    description: str | None
    unit: float | None
    unit_size: float | None
    weight: float | None
    price: float | None
    category: str | None
    created_at: datetime
    updated_at: datetime | None


class ProductForPricingDTO(BaseModel):
    id: int
    sku: str
    unit: float
    price: float
