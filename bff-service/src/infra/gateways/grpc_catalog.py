from typing import List, Optional

import grpc
from generated import catalog_pb2, catalog_pb2_grpc
from src.application.dtos.catalog_dto import ProductDTO
from src.application.dtos.pagination import PaginatedResponse
from src.application.ports.catalog_gateway import ICatalogGateway


class CatalogGrpcGateway(ICatalogGateway):
    def __init__(self, channel: grpc.aio.Channel):
        self.stub = catalog_pb2_grpc.CatalogServiceStub(channel)

    async def validate_stock(self, item_ids: List[int]) -> List[int]:
        request = catalog_pb2.GetProductsRequest(product_ids=item_ids)
        response = await self.stub.GetProductsForValidation(request)
        return list(response.product_ids)

    async def get_products_for_order_summary(
        self, product_ids: List[int]
    ) -> List[ProductDTO]:
        request = catalog_pb2.GetProductsRequest(product_ids=product_ids)
        response = await self.stub.GetProducts(request)
        products = [
            ProductDTO(
                id=product.id,
                uuid=product.uuid,
                name=product.name,
                sku=product.sku,
                brand=product.brand,
                description=product.description,
                unit=product.unit,
                unit_size=product.unit_size,
                weight=product.weight,
                price=product.price,
                category=product.category,
            )
            for product in response.products
        ]

        return products

    async def get_paginated_products(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> PaginatedResponse:
        request = catalog_pb2.GetPaginatedProductsRequest(
            page_size=page_size, page_token=page_token, search_text=search_text
        )
        response = await self.stub.GetPaginatedProducts(request)

        products = [
            ProductDTO(
                id=product.id,
                uuid=product.uuid,
                name=product.name,
                sku=product.sku,
                brand=product.brand,
                description=product.description,
                unit=product.unit,
                unit_size=product.unit_size,
                weight=product.weight,
                price=product.price,
                category=product.category,
            )
            for product in response.products
        ]

        return PaginatedResponse(
            data=products,
            next_page_token=response.next_page_token,
            has_more=response.has_more,
        )
