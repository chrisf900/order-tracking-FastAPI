from abc import ABC, abstractmethod
from typing import List, Optional

from src.application.dtos.catalog_dto import ProductDTO
from src.application.dtos.pagination import PaginatedResponse


class ICatalogGateway(ABC):

    @abstractmethod
    async def validate_stock(self, item_ids: List[int]) -> List[int]:
        pass

    @abstractmethod
    async def get_products_for_order_summary(
        self, product_ids: List[int]
    ) -> List[ProductDTO]:
        pass

    @abstractmethod
    async def get_paginated_products(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> PaginatedResponse:
        pass
