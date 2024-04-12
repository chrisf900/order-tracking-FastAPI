import grpc
from generated import pricing_pb2, pricing_pb2_grpc
from src.application.dtos.order import OrderItemDTO
from src.application.ports import catalog_gateway
from src.application.usecases.calculate_order_total import CalculateOrderTotalUseCase
from src.domain.exceptions import InvalidTotalAmount, ProductNotFound
from src.domain.services.order_calculator import OrderCalculator
from src.infra.gateways.catalog.grpc_catalog import CatalogGrpcGateway


class PricingService(pricing_pb2_grpc.PricingServiceServicer):
    def __init__(self, use_case: CalculateOrderTotalUseCase):
        self.use_case = use_case

    async def CalculateTotal(self, request, context):
        items = [
            OrderItemDTO(
                uuid=item.uuid, product_id=item.product_id, quantity=item.quantity
            )
            for item in request.items
        ]

        try:
            total = await self.use_case.execute(items=items)
        except ProductNotFound:
            await context.abort(grpc.StatusCode.NOT_FOUND, "PRODUCTS_NOT_FOUND")
        except InvalidTotalAmount:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "INVALID_TOTAL_AMOUNT"
            )

        return pricing_pb2.TotalCalculationResponse(total_amount=total)
