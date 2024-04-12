from typing import List

from src.application.dtos.product_dto import ProductDTO
from src.domain.exceptions import ProductNotFoundError
from src.domain.ports.brand_repository import IBrandRepository
from src.domain.ports.category_repository import ICategoryRepository
from src.domain.ports.product_repository import IProductRepository


class GetProductsUseCase:
    def __init__(
        self,
        product_repo: IProductRepository,
        brand_repo: IBrandRepository,
        category_repo: ICategoryRepository,
    ):
        self.product_repo = product_repo
        self.brand_repo = brand_repo
        self.category_repo = category_repo

    async def execute(
        self,
        product_ids: List[int],
    ) -> List[ProductDTO]:

        products = await self.product_repo.get_products_by_ids(product_ids=product_ids)

        brand_uuids = {p.brand_uuid for p in products if p.brand_uuid}
        brands = await self.brand_repo.get_brands_by_uuid(brand_uuids=brand_uuids)
        brand_map = {brand.uuid: brand.name for brand in brands}

        category_uuids = {p.category_uuid for p in products if p.category_uuid}
        categories = await self.category_repo.get_categories_by_uuid(
            category_uuids=category_uuids
        )
        category_map = {category.uuid: category.name for category in categories}

        product_dto_list = [
            ProductDTO(
                id=product.id,
                uuid=str(product.uuid),
                name=product.name,
                sku=product.sku,
                brand=brand_map.get(product.brand_uuid),
                category=category_map.get(product.category_uuid),
                description=product.description,
                unit=product.unit,
                unit_size=product.unit_size,
                weight=product.weight,
                price=product.price,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
            for product in products
        ]

        return product_dto_list


class GetProductsForValidationUseCase:
    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_ids: List[int]) -> List[int]:
        products = await self.product_repo.get_products_for_pricing(
            product_ids=product_ids
        )

        product_ids = [product.id for product in products]

        return product_ids
