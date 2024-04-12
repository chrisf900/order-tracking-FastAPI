from abc import ABC, abstractmethod
from typing import List, Optional

from src.application.dtos.pagination import PaginatedResultDTO
from src.domain.entities.product import ProductEntity, ProductForPricingEntity


class IProductRepository(ABC):
    @abstractmethod
    async def get_products_for_pricing(
        self, product_ids: List[int]
    ) -> List[ProductForPricingEntity]:
        raise NotImplementedError("IProductRepository method not implemented")

    @abstractmethod
    async def get_paginated_products_data(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> PaginatedResultDTO[ProductEntity]:
        raise NotImplementedError("IProductRepository method not implemented")

    @abstractmethod
    async def get_products_by_ids(self, product_ids: List[int]) -> List[ProductEntity]:
        raise NotImplementedError("IProductRepository method not implemented")
