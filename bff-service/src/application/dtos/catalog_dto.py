from dataclasses import dataclass

from pydantic import BaseModel


class ProductDTO(BaseModel):
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


class OrderProductDTO(BaseModel):
    id: int
    uuid: str
    name: str
    quantity: int
    sku: str | None = None
    brand: str | None = None
    description: str | None = None
    unit: float | None = None
    unit_size: float | None = None
    weight: float | None = None
    price: float | None = None
    category: str | None = None
