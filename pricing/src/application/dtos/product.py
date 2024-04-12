from pydantic import BaseModel


class ProductForPricingDTO(BaseModel):
    id: int
    sku: str
    unit: float
    price: float
