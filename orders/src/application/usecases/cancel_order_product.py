from src.application.dtos.order_dto import OrderDTO
from src.domain.exceptions import CancelOrderIsNotAvailable, OrderNotFoundError
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.services.order_status_machine_service import DeliveryStateMachine


class CancelOrderUseCase:
    def __init__(
        self,
        order_repo: IOrderRepository,
    ):
        self.order_repo = order_repo

    async def execute(self, order_uuid: str) -> OrderDTO:
        order = await self.order_repo.get_order_by_uuid(order_uuid=order_uuid)

        if not order:
            raise OrderNotFoundError()

        if order.delivery_status not in ["DRAFT", "IN_PROGRESS"]:
            raise CancelOrderIsNotAvailable()

        dsm = DeliveryStateMachine(state=order.delivery_status, order=order)
        dsm.change("CANCELLED")

        return OrderDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
