from uuid import UUID

from src.application.dtos.orders_dto import OrderDTO
from src.application.ports.orders_gateway import IOrdersGateway


class CancelOrderUseCase:
    def __init__(
        self,
        order_gateway: IOrdersGateway,
    ):
        self.order_gateway = order_gateway

    async def execute(self, order_uuid: UUID) -> OrderDTO:
        return await self.order_gateway.cancel_order(order_uuid=order_uuid)
