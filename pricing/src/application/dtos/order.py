from pydantic import BaseModel


class OrderItemDTO(BaseModel):
    uuid: str
    product_id: int
    quantity: float
