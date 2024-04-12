from uuid import UUID

from fastapi import APIRouter, Depends, status, Header
from src.api.dependencies import (
    get_catalog_gateway,
    get_order_gateway,
    get_pricing_gateway,
)
from src.api.docs.openapi import ORDER_RESPONSES
from src.api.v1.schemas.schema import (
    CreateOrderRequest,
    OrderSchema,
    OrderStatusSchema,
    OrderWithProductsSchema,
)
from src.application.dtos.orders_dto import ItemDTO
from src.application.exceptions import BFFServiceError
from src.application.usecases.cancel_order import CancelOrderUseCase
from src.application.usecases.create_order import CreateOrderUseCase
from src.application.usecases.get_order_summary import GetOrderSummaryUseCase
from src.application.usecases.update_order import UpdateOrderStatusUseCase
from src.infra.gateways.grpc_catalog import CatalogGrpcGateway
from src.infra.gateways.grpc_orders import OrdersGrpcGateway
from src.infra.gateways.grpc_pricing import PricingGrpcGateway

router = APIRouter()


@router.get(
    "/{order_uuid}",
    summary="Get order summary",
    response_model=OrderWithProductsSchema,
    responses=ORDER_RESPONSES,
)
async def get_order(
    order_uuid: UUID,
    order_gateway: OrdersGrpcGateway = Depends(get_order_gateway),
    catalog_gateway: CatalogGrpcGateway = Depends(get_catalog_gateway),
):
    """
    Retrieve full Order enriched with product data.
    """
    use_case = GetOrderSummaryUseCase(
        order_gateway=order_gateway, catalog_gateway=catalog_gateway
    )
    return await use_case.execute(order_uuid=order_uuid)


@router.patch(
    "/{order_uuid}/status",
    summary="Update order delivery status",
    response_model=OrderSchema,
    responses=ORDER_RESPONSES,
)
async def update_order_delivery_status(
    order_uuid: UUID,
    payload: OrderStatusSchema,
    order_gateway: OrdersGrpcGateway = Depends(get_order_gateway),
):
    """
    Updates the delivery status of an existing order.
    """
    use_case = UpdateOrderStatusUseCase(order_gateway=order_gateway)
    return await use_case.execute(
        order_uuid=order_uuid, new_status=payload.update_status
    )


@router.post(
    "/",
    response_model=OrderSchema,
    summary="Create a new order",
    status_code=status.HTTP_201_CREATED,
    responses=ORDER_RESPONSES,
)
async def create_order(
    payload: CreateOrderRequest,
    idempotency_key: str = Header(None),
    catalog_gateway: CatalogGrpcGateway = Depends(get_catalog_gateway),
    pricing_gateway: PricingGrpcGateway = Depends(get_pricing_gateway),
    order_gateway: OrdersGrpcGateway = Depends(get_order_gateway),
):
    """
    Creates an order by orchestrating services:
    - **Catalog**: Validates product availability.
    - **Pricing**: Confirms current item prices.
    - **Orders**: Finalizes the transaction.
    """
    use_case = CreateOrderUseCase(
        catalog_gateway=catalog_gateway,
        pricing_gateway=pricing_gateway,
        order_gateway=order_gateway,
    )

    items = [
        ItemDTO(
            uuid=item.uuid,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        for item in payload.items
    ]

    return await use_case.execute(
        user_uuid=payload.user_uuid,
        items_request=items,
    )


@router.patch(
    "/{order_uuid}/cancellation",
    summary="Cancel an order",
    response_model=OrderSchema,
    responses=ORDER_RESPONSES,
)
async def cancel_order(
    order_uuid: UUID,
    order_gateway: OrdersGrpcGateway = Depends(get_order_gateway),
):
    """
    Initiate the order cancellation flow.
    """
    use_case = CancelOrderUseCase(order_gateway=order_gateway)
    return await use_case.execute(order_uuid=order_uuid)
