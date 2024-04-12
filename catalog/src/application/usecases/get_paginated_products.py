from typing import Optional

from src.application.dtos.pagination import PaginatedResultDTO
from src.application.dtos.product_dto import ProductDTO
from src.infra.repositories.brand import BrandRepository
from src.infra.repositories.category import CategoryRepository
from src.infra.repositories.product import ProductRepository


class GetPaginatedProductsUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        brand_repo: BrandRepository,
        category_repo: CategoryRepository,
    ):
        self.product_repo = product_repo
        self.brand_repo = brand_repo
        self.category_repo = category_repo

    async def execute(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> PaginatedResultDTO[ProductDTO]:
        paginated_products = await self.product_repo.get_paginated_products_data(
            page_size=page_size, page_token=page_token, search_text=search_text
        )
        products = paginated_products.items

        brand_uuids = {p.brand_uuid for p in products if p.brand_uuid}
        brands = await self.brand_repo.get_brands_by_uuid(brand_uuids=brand_uuids)
        brand_map = {brand.uuid: brand.name for brand in brands}

        category_uuids = {p.category_uuid for p in products if p.category_uuid}
        categories = await self.category_repo.get_categories_by_uuid(
            category_uuids=category_uuids
        )
        category_map = {category.uuid: category.name for category in categories}

        product_dtos = []
        for product in products:
            dto = ProductDTO(
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
            product_dtos.append(dto)

        return PaginatedResultDTO(
            items=product_dtos,
            next_cursor=paginated_products.next_cursor,
            has_more=paginated_products.has_more,
        )
