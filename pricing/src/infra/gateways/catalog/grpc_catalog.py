from typing import List

import grpc
from generated.shared_protos import catalog_pb2, catalog_pb2_grpc
from src.application.dtos.product import ProductForPricingDTO
from src.application.ports.catalog_gateway import ICatalogGateway


class CatalogGrpcGateway(ICatalogGateway):
    def __init__(self, channel: grpc.aio.Channel):
        self.stub = catalog_pb2_grpc.CatalogServiceStub(channel)

    async def get_products(
        self, order_items_ids: List[int]
    ) -> List[ProductForPricingDTO]:
        response = await self.stub.GetProductsForPricing(
            catalog_pb2.GetProductsRequest(product_ids=order_items_ids)
        )

        products = []
        for product in response.products:
            products.append(
                ProductForPricingDTO(
                    id=product.id,
                    sku=product.sku,
                    unit=product.unit,
                    price=product.price,
                )
            )

        return products
