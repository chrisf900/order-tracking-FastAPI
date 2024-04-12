from typing import Optional

from src.application.ports.catalog_gateway import ICatalogGateway


class GetPaginatedProductsUseCase:
    def __init__(
        self,
        catalog_gateway: ICatalogGateway,
    ):
        self.catalog_gateway = catalog_gateway

    async def execute(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ):
        paginated_products = await self.catalog_gateway.get_paginated_products(
            page_size=page_size, page_token=page_token, search_text=search_text
        )
        return paginated_products
