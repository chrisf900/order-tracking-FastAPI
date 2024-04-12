from typing import Optional

from fastapi import APIRouter, Depends, Query
from src.api.dependencies import get_catalog_gateway
from src.application.dtos.pagination import PaginatedResponse
from src.application.usecases.get_paginated_products import GetPaginatedProductsUseCase
from src.infra.gateways.grpc_catalog import CatalogGrpcGateway

router = APIRouter()


@router.get(
    "/catalog",
    response_model=PaginatedResponse,
)
async def get_paginated_products(
    size: int = Query(10, ge=1, le=50),
    page_token: Optional[str] = Query(None),
    search_text: Optional[str] = Query(None, min_length=3),
    catalog_gateway: CatalogGrpcGateway = Depends(get_catalog_gateway),
):
    """
    Get a paginated list of products from the catalog.
    - **size**: Number of items per page.
    - **page_token**: The token received from a previous request to fetch the next set of results.
    - **search_text**: Optional string to filter products by name.
    """
    use_case = GetPaginatedProductsUseCase(catalog_gateway=catalog_gateway)
    results = await use_case.execute(
        page_size=size, page_token=page_token, search_text=search_text
    )

    return PaginatedResponse(
        data=results.data,
        next_page_token=results.next_page_token,
        has_more=results.has_more,
    )
