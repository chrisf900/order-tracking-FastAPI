from src.application.ports.orders_gateway import IOrdersGateway


class UpdateOrderStatusUseCase:
    def __init__(
        self,
        order_gateway: IOrdersGateway,
    ):
        self.order_gateway = order_gateway

    async def execute(self, order_uuid: str, new_status: str):
        try:
            order = await self.order_gateway.update_order_status(
                order_uuid=order_uuid, status=new_status
            )
        except Exception:
            raise
        return order
