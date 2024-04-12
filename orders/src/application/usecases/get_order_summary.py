import asyncio

from src.application.dtos.order_dto import OrderItemDTO, OrderWithItemsDTO
from src.domain.repositories.order_detail_repository import IOrderDetailRepository
from src.domain.repositories.order_repository import IOrderRepository


class GetOrderSummaryUseCase:
    def __init__(
        self, order_repo: IOrderRepository, order_detail_repo: IOrderDetailRepository
    ):
        self.order_repo = order_repo
        self.order_detail_repo = order_detail_repo

    async def execute(self, order_uuid: str) -> OrderWithItemsDTO:
        order = await self.order_repo.get_order_by_uuid(order_uuid=order_uuid)
        order_detail = await self.order_detail_repo.get_order_detail_by_order_uuid(
            order_uuid=order_uuid
        )

        order_items = [
            OrderItemDTO(
                uuid=item.uuid,
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in order_detail
        ]

        return OrderWithItemsDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            items=order_items,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
