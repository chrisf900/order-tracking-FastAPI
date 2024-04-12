from src.application.dtos.order_dto import OrderDTO
from src.domain.repositories.order_repository import IOrderRepository


class GetOrderUseCase:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    async def execute(self, order_uuid: str) -> OrderDTO:
        order = await self.order_repo.get_order_by_uuid(order_uuid=order_uuid)

        return OrderDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
