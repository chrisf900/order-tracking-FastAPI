from typing import List

from src.application.dtos.product_dto import ProductForPricingDTO
from src.domain.ports.product_repository import IProductRepository


class GetProductsForPricingUseCase:
    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_ids: List[int]):
        products = await self.product_repo.get_products_for_pricing(
            product_ids=product_ids
        )

        products_dto = [
            ProductForPricingDTO(
                id=product.id,
                sku=product.sku,
                unit=product.unit,
                price=product.price,
            )
            for product in products
        ]

        return products_dto
