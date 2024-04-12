from src.api.exceptions import OrderNotFoundError
from src.interfaces import IOrdersGateway


class GetOrderUseCase:
    def __init__(
        self,
        order_gateway: IOrdersGateway,
    ):
        self.order_gateway = order_gateway

    async def execute(self, order_uuid: str):
        return await self.order_gateway.get_order_by_uuid(order_uuid=order_uuid)
