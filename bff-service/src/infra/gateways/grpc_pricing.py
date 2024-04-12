import grpc
from generated import pricing_pb2, pricing_pb2_grpc
from src.application.dtos.orders_dto import ItemDTO
from src.application.ports.pricing_gateway import IPricingGateway


class PricingGrpcGateway(IPricingGateway):
    def __init__(self, channel: grpc.aio.Channel):
        self.stub = pricing_pb2_grpc.PricingServiceStub(channel)

    async def calculate_total(self, items: ItemDTO) -> float:
        grpc_items = [
            pricing_pb2.ItemToCalculate(
                product_id=int(item.product_id), quantity=float(item.quantity)
            )
            for item in items
        ]

        request = pricing_pb2.OrderItemsRequest(items=grpc_items)
        response = await self.stub.CalculateTotal(request)
        return response.total_amount
