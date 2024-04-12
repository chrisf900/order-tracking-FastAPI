from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.dtos.pagination import PaginatedResultDTO
from src.domain.entities.product import ProductEntity, ProductForPricingEntity
from src.domain.ports.product_repository import IProductRepository
from src.infra.db.models.product import Product
from src.infra.utils import decode_page_token, encode_page_token


class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_products_for_pricing(
        self, product_ids: List[int]
    ) -> List[ProductForPricingEntity]:
        product_ids = [int(pid) for pid in product_ids]
        query = select(Product).where(Product.id.in_(product_ids))
        result = await self.session.execute(query)

        products = result.scalars().all()

        return [
            ProductForPricingEntity(
                id=product.id,
                sku=product.sku,
                unit=product.unit,
                price=product.price,
            )
            for product in products
        ]

    async def get_paginated_products_data(
        self,
        page_size: int = 10,
        page_token: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> PaginatedResultDTO[ProductEntity]:
        query = select(Product)

        if search_text:
            query = query.where(Product.name.ilike(f"%{search_text}%"))

        if page_token:
            page_token = decode_page_token(page_token)
            query = query.where(Product.created_at < page_token)

        query = query.order_by(Product.created_at.desc()).limit(page_size + 1)

        result = await self.session.execute(query)

        products = result.scalars().all()

        products = [
            ProductEntity(
                id=product.id,
                uuid=product.uuid,
                sku=product.sku,
                unit=product.unit,
                price=product.price,
                name=product.name,
                brand_uuid=product.brand_uuid,
                description=product.description,
                unit_size=product.unit_size,
                weight=product.weight,
                category_uuid=product.category_uuid,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
            for product in products[:page_size]
        ]

        has_more = len(products) > page_size

        if has_more:
            last_item = products[page_size - 1]
            raw_token = f"{last_item.created_at.isoformat()}|{last_item.id}"

            next_cursor = encode_page_token(raw_token)
        else:
            next_cursor = None

        return PaginatedResultDTO(
            items=products, next_cursor=next_cursor, has_more=has_more
        )

    async def get_products_by_ids(self, product_ids: List[int]) -> List[ProductEntity]:
        query = select(Product).where(Product.id.in_(product_ids))
        result = await self.session.execute(query)

        products = result.scalars().all()

        return [
            ProductEntity(
                id=product.id,
                uuid=product.uuid,
                sku=product.sku,
                unit=product.unit,
                price=product.price,
                name=product.name,
                brand_uuid=product.brand_uuid,
                description=product.description,
                unit_size=product.unit_size,
                weight=product.weight,
                category_uuid=product.category_uuid,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
            for product in products
        ]
