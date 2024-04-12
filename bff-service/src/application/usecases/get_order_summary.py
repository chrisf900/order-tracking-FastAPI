from src.application.dtos.catalog_dto import OrderProductDTO
from src.application.dtos.orders_dto import OrderWithProductsDTO
from src.application.ports.catalog_gateway import ICatalogGateway
from src.application.ports.orders_gateway import IOrdersGateway


class GetOrderSummaryUseCase:
    def __init__(self, order_gateway: IOrdersGateway, catalog_gateway: ICatalogGateway):
        self.order_gateway = order_gateway
        self.catalog_gateway = catalog_gateway

    async def execute(self, order_uuid: str) -> OrderWithProductsDTO:
        order = await self.order_gateway.get_order_summary_by_order_uuid(
            order_uuid=order_uuid
        )

        product_ids = {item.product_id for item in order.items}
        quantity_map = {item.product_id: item.quantity for item in order.items}
        products = await self.catalog_gateway.get_products_for_order_summary(
            product_ids=list(product_ids)
        )

        products_map = {item.id: item for item in products}

        enriched_items = []
        for item in order.items:
            product_info = products_map.get(item.product_id)
            product_quantity = quantity_map.get(item.product_id)
            enriched_items.append(
                OrderProductDTO(
                    id=product_info.id,
                    uuid=product_info.uuid,
                    name=product_info.name,
                    quantity=product_quantity,
                    sku=product_info.sku,
                    brand=product_info.brand,
                    description=product_info.description,
                    unit=product_info.unit,
                    unit_size=product_info.unit_size,
                    weight=product_info.weight,
                    price=product_info.price,
                    category=product_info.category,
                )
            )

        return OrderWithProductsDTO(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            items=enriched_items,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
