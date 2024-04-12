import logging

from generated import catalog_pb2, catalog_pb2_grpc
from src.application.dtos.product_dto import ProductForPricingDTO
from src.application.usecases.get_paginated_products import GetPaginatedProductsUseCase
from src.application.usecases.get_products import (
    GetProductsForValidationUseCase,
    GetProductsUseCase,
)
from src.application.usecases.get_products_for_pricing import (
    GetProductsForPricingUseCase,
)
from src.config.db import AsyncSessionLocal
from src.infra.repositories.brand import BrandRepository
from src.infra.repositories.category import CategoryRepository
from src.infra.repositories.product import ProductRepository
from src.interfaces.grpc.utils import to_proto_timestamp

logger = logging.getLogger(__name__)


class CatalogService(catalog_pb2_grpc.CatalogServiceServicer):
    async def GetProductsForPricing(self, request, context):
        async with AsyncSessionLocal() as session:
            product_repository = ProductRepository(session)
            use_case = GetProductsForPricingUseCase(product_repo=product_repository)

            products = await use_case.execute(product_ids=request.product_ids)

            products = [
                catalog_pb2.GetProductsForPricing(
                    id=product_dto.id,
                    sku=product_dto.sku,
                    unit=product_dto.unit,
                    price=product_dto.price,
                )
                for product_dto in products
            ]

            return catalog_pb2.GetProductForPricingResponse(products=products)

    async def GetProductsForValidation(self, request, context):
        async with AsyncSessionLocal() as session:
            product_repository = ProductRepository(session)
            use_case = GetProductsForValidationUseCase(product_repo=product_repository)

            product_ids = await use_case.execute(product_ids=request.product_ids)

            return catalog_pb2.GetProductsForValidationResponse(product_ids=product_ids)

    async def GetProducts(self, request, context):
        async with AsyncSessionLocal() as session:
            product_repository = ProductRepository(session)
            brand_repository = BrandRepository(session)
            category_repository = CategoryRepository(session)

            use_case = GetProductsUseCase(
                product_repo=product_repository,
                brand_repo=brand_repository,
                category_repo=category_repository,
            )

            products = await use_case.execute(product_ids=request.product_ids)

            products = [
                catalog_pb2.Product(
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
                    created_at=to_proto_timestamp(product.created_at),
                    updated_at=to_proto_timestamp(product.updated_at),
                )
                for product in products
            ]

            return catalog_pb2.GetProductsResponse(products=products)

    async def GetPaginatedProducts(self, request, context):
        async with AsyncSessionLocal() as session:
            product_repository = ProductRepository(session)
            brand_repository = BrandRepository(session)
            category_repository = CategoryRepository(session)

            use_case = GetPaginatedProductsUseCase(
                product_repo=product_repository,
                brand_repo=brand_repository,
                category_repo=category_repository,
            )

            results = await use_case.execute(
                page_size=request.page_size,
                page_token=request.page_token,
                search_text=request.search_text,
            )

            paginated_products = [
                catalog_pb2.Product(
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
                    created_at=to_proto_timestamp(product.created_at),
                    updated_at=to_proto_timestamp(product.updated_at),
                )
                for product in results.items
            ]

            return catalog_pb2.GetPaginatedProductsResponse(
                products=paginated_products,
                next_page_token=results.next_cursor,
                has_more=results.has_more,
            )
