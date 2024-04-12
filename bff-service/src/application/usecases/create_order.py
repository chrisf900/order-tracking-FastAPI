from typing import List

from src.application.dtos.orders_dto import ItemDTO, OrderDTO
from src.application.ports.catalog_gateway import ICatalogGateway
from src.application.ports.orders_gateway import IOrdersGateway
from src.application.ports.pricing_gateway import IPricingGateway


class CreateOrderUseCase:
    def __init__(
        self,
        catalog_gateway: ICatalogGateway,
        pricing_gateway: IPricingGateway,
        order_gateway: IOrdersGateway,
    ):
        self.catalog_gateway = catalog_gateway
        self.pricing_gateway = pricing_gateway
        self.order_gateway = order_gateway

    async def execute(self, user_uuid: str, items_request: List[ItemDTO]) -> OrderDTO:
        item_ids = [item.product_id for item in items_request]
        validated_item_ids = await self.catalog_gateway.validate_stock(
            item_ids=item_ids
        )

        if not validated_item_ids:
            raise ValueError("Uno o más productos no tienen stock disponible")

        validated_items = [
            item for item in items_request if item.product_id in item_ids
        ]

        total_amount = await self.pricing_gateway.calculate_total(items=validated_items)

        new_order = await self.order_gateway.create_order(
            user_uuid=user_uuid, total_amount=total_amount, items=validated_items
        )

        return new_order
