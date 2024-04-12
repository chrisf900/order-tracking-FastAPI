from dataclasses import dataclass
from datetime import datetime


@dataclass
class BrandDTO:
    uuid: str
    brand: str


@dataclass
class CategoryDTO:
    uuid: str
    category: str


@dataclass
class ProductDTO:
    id: int
    uuid: str
    name: str
    sku: str | None = None
    brand: str | None = None
    description: str | None = None
    unit: float | None = None
    unit_size: float | None = None
    weight: float | None = None
    price: float | None = None
    category: str | None = None
    created_at: datetime | None  = None
    updated_at: datetime | None  = None
