from typing import List

from src.application.dtos.order_dto import AddProductToOrderDTO, OrderDTO
from src.domain.entities.order_detail import OrderDetailEntity
from src.domain.exceptions import InvalidTotalAmount
from src.domain.repositories.order_detail_repository import IOrderDetailRepository
from src.domain.repositories.order_repository import IOrderRepository


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        order_detail_repository: IOrderDetailRepository,
    ):
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository

    async def execute(
        self,
        user_uuid: str,
        total_amount: float,
        items: List[AddProductToOrderDTO],
    ) -> OrderDTO:
        if total_amount <= 0:
            raise InvalidTotalAmount()

        order = await self.order_repository.create_order(
            user_uuid=user_uuid, total_amount=total_amount
        )

        items_to_add = [
            OrderDetailEntity(
                product_id=item.product_id,
                order_uuid=order.uuid,
                quantity=item.quantity,
                uuid=item.uuid,
            )
            for item in items
        ]

        await self.order_detail_repository.add_order_products(
            order_uuid=order.uuid, products=items_to_add
        )

        return OrderDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
