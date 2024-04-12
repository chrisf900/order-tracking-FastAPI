from typing import List

from src.application.dtos.order_dto import OrderItemDTO
from src.domain.exceptions import OrderDetailNotFoundError
from src.domain.repositories.order_detail_repository import IOrderDetailRepository


class GetOrderItemsUseCase:
    def __init__(self, order_detail_repo: IOrderDetailRepository):
        self.order_detail_repo = order_detail_repo

    async def execute(self, order_uuid: str) -> List[OrderItemDTO]:
        order_detail = await self.order_detail_repo.get_order_detail_by_order_uuid(
            order_uuid=order_uuid
        )

        if not order_detail:
            raise OrderDetailNotFoundError()

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

        return order_items
