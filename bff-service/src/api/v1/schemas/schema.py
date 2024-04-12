from datetime import datetime
from typing import List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator

M = TypeVar("M")


class User(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    phone_number: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None = None
    group_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    uuid: str
    name: str
    quantity: float
    sku: str | None = None
    brand: str | None = None
    description: str | None = None
    unit: float | None = None
    unit_size: float | None = None
    weight: float | None = None
    price: float | None = None
    category: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OrderStatusSchema(BaseModel):
    update_status: str

    @field_validator("update_status")
    @classmethod
    def update_status_validation(cls, value: str) -> str:
        states = ["PREPARING_FOR_DELIVERY", "DELIVERED", "CANCELLED"]
        if value not in states:
            raise ValueError("Invalid state name")
        return value


class AddOrderProductsSchema(BaseModel):
    product_uuids: list[UUID]


class CreateOrderSchema(BaseModel):
    product_uuids: list[UUID]


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    password: str


class UpdateUserContactInfoSchema(BaseModel):
    email: EmailStr | None = None
    phone_number: int | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, values):
        if not values:
            raise ValueError("email field or phone_number field is required")
        return values


class OrderItemSchema(BaseModel):
    uuid: str
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class CreateOrderRequest(BaseModel):
    user_uuid: str
    items: List[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)


class OrderWithProductsSchema(BaseModel):
    uuid: str
    user_uuid: str
    delivery_status: str
    total_amount: float
    items: List[ProductSchema]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
