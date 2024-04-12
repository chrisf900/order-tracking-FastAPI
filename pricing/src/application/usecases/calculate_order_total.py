from src.application.dtos.order import OrderItemDTO
from src.application.ports.catalog_gateway import ICatalogGateway
from src.domain.exceptions import InvalidTotalAmount, ProductNotFound
from src.domain.services.order_calculator import OrderCalculator
from src.infra.gateways.catalog.grpc_catalog import CatalogGrpcGateway


class CalculateOrderTotalUseCase:
    def __init__(
        self,
        catalog_gateway: ICatalogGateway,
        order_calculator: OrderCalculator,
    ):
        self.catalog_gateway = catalog_gateway
        self.order_calculator = order_calculator

    async def execute(self, items: OrderItemDTO) -> float:
        product_ids = [item.product_id for item in items]
        catalog_products = await self.catalog_gateway.get_products(
            order_items_ids=product_ids
        )

        if not catalog_products:
            raise ProductNotFound()

        total = self.order_calculator.calculate_total(
            items=items, catalog_products=catalog_products
        )

        if total <= 0:
            raise InvalidTotalAmount()

        return total
