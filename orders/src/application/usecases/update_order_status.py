from src.application.dtos.order_dto import OrderDTO
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.services.order_status_machine_service import DeliveryStateMachine


class UpdateOrderStatusUseCase:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    async def execute(self, order_uuid: str, new_status: str) -> OrderDTO:
        order = await self.order_repo.get_order_by_uuid(order_uuid=order_uuid)

        dsm = DeliveryStateMachine(state=order.delivery_status, order=order)
        dsm.change(new_status)

        await self.order_repo.update_order_status(
            order_uuid=order.uuid, new_status=new_status
        )

        return OrderDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
