import logging

import grpc
from generated import orders_pb2, orders_pb2_grpc
from src.application.usecases.cancel_order_product import CancelOrderUseCase
from src.application.usecases.create_order import CreateOrderUseCase
from src.application.usecases.get_order import GetOrderUseCase
from src.application.usecases.get_order_summary import GetOrderSummaryUseCase
from src.application.usecases.get_order_with_items import GetOrderItemsUseCase
from src.application.usecases.update_order_status import UpdateOrderStatusUseCase
from src.config.db import AsyncSessionLocal
from src.domain.exceptions import (
    CancelOrderIsNotAvailable,
    InvalidDeliveryStatusTransition,
    InvalidStatusName,
    InvalidTotalAmount,
    OrderCreationError,
    OrderDetailCreationError,
    OrderDetailNotFoundError,
    OrderNotFoundError,
    OrderStatusNotUpdatedError,
)
from src.infra.repositories.order import OrderRepository
from src.infra.repositories.order_detail import OrderDetailRepository
from src.interfaces.grpc.utils import to_proto_timestamp

logger = logging.getLogger(__name__)


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    async def GetOrder(self, request, context):
        async with AsyncSessionLocal() as session:
            order_repository = OrderRepository(session)
            use_case = GetOrderUseCase(order_repo=order_repository)

            try:
                order = await use_case.execute(order_uuid=request.uuid)
            except OrderNotFoundError:
                await context.abort(grpc.StatusCode.NOT_FOUND, "ORDER_NOT_FOUND")

            return orders_pb2.OrderResponse(
                uuid=order.uuid,
                user_uuid=order.user_uuid,
                delivery_status=order.delivery_status,
                total_amount=order.total_amount,
                created_at=to_proto_timestamp(order.created_at),
                updated_at=to_proto_timestamp(order.updated_at),
            )

    async def GetOrderItems(self, request, context):
        async with AsyncSessionLocal() as session:
            try:
                order_detail_repository = OrderDetailRepository(session)
                use_case = GetOrderItemsUseCase(
                    order_detail_repo=order_detail_repository
                )

                order_items = await use_case.execute(order_uuid=request.uuid)
            except OrderDetailNotFoundError:
                await context.abort(grpc.StatusCode.NOT_FOUND, "ORDER_ITEMS_NOT_FOUND")

            items = [
                orders_pb2.OrderItemResponse(
                    uuid=item.uuid,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    created_at=to_proto_timestamp(item.created_at),
                    updated_at=to_proto_timestamp(item.updated_at),
                )
                for item in order_items
            ]
            return orders_pb2.OrderItemsResponse(
                order_uuid=request.uuid, order_items=items
            )

    async def CreateOrder(self, request, context):
        async with AsyncSessionLocal() as session:
            try:
                order_detail_repo = OrderDetailRepository(session=session)
                order_repo = OrderRepository(session=session)

                create_order_use_case = CreateOrderUseCase(
                    order_repository=order_repo,
                    order_detail_repository=order_detail_repo,
                )

                order = await create_order_use_case.execute(
                    user_uuid=request.user_uuid,
                    total_amount=request.total_amount,
                    items=request.items,
                )
            except (OrderCreationError, OrderDetailCreationError):
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT, "ORDER_NOT_CREATED"
                )
            except InvalidTotalAmount:
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT, "INVALID_TOTAL_AMOUNT"
                )

            return orders_pb2.OrderResponse(
                uuid=order.uuid,
                user_uuid=order.user_uuid,
                delivery_status=order.delivery_status,
                total_amount=order.total_amount,
                created_at=to_proto_timestamp(order.created_at),
                updated_at=to_proto_timestamp(order.updated_at),
            )

    async def UpdateOrderStatus(self, request, context):
        async with AsyncSessionLocal() as session:
            try:
                order_repo = OrderRepository(session=session)
                use_case = UpdateOrderStatusUseCase(order_repo=order_repo)
                order = await use_case.execute(
                    order_uuid=request.order_uuid, new_status=request.status
                )

                if not order:
                    await context.abort(grpc.StatusCode.NOT_FOUND, "ORDER_NOT_FOUND")

                return orders_pb2.OrderResponse(
                    uuid=order.uuid,
                    user_uuid=order.user_uuid,
                    delivery_status=order.delivery_status,
                    total_amount=order.total_amount,
                    created_at=to_proto_timestamp(order.created_at),
                    updated_at=to_proto_timestamp(order.updated_at),
                )
            except InvalidDeliveryStatusTransition:
                await context.abort(
                    grpc.StatusCode.FAILED_PRECONDITION,
                    "INVALID_ORDER_STATUS_TRANSITION",
                )
            except InvalidStatusName:
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT, "INVALID_STATUS_NAME"
                )
            except OrderStatusNotUpdatedError:
                await context.abort(
                    grpc.StatusCode.FAILED_PRECONDITION, "ORDER_STATUS_NOT_UPDATED"
                )

    async def CancelOrder(self, request, context):
        async with AsyncSessionLocal() as session:
            try:
                order_repo = OrderRepository(session=session)
                use_case = CancelOrderUseCase(order_repo=order_repo)
                order = await use_case.execute(order_uuid=request.uuid)
            except OrderNotFoundError:
                await context.abort(grpc.StatusCode.NOT_FOUND, "ORDER_NOT_FOUND")
            except CancelOrderIsNotAvailable:
                await context.abort(
                    grpc.StatusCode.FAILED_PRECONDITION,
                    "ACTION_CANCEL_ORDER_NOT_AVAILABLE",
                )

            return orders_pb2.OrderResponse(
                uuid=order.uuid,
                user_uuid=order.user_uuid,
                delivery_status=order.delivery_status,
                total_amount=order.total_amount,
                created_at=to_proto_timestamp(order.created_at),
                updated_at=to_proto_timestamp(order.updated_at),
            )

    async def GetOrderSummary(self, request, context):
        async with AsyncSessionLocal() as session:
            try:
                order_repository = OrderRepository(session)
                order_detail_repository = OrderDetailRepository(session)
                use_case = GetOrderSummaryUseCase(
                    order_repo=order_repository,
                    order_detail_repo=order_detail_repository,
                )
                order_with_items = await use_case.execute(order_uuid=str(request.uuid))

                order_items = [
                    orders_pb2.OrderItemResponse(
                        uuid=item.uuid,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        created_at=to_proto_timestamp(item.created_at),
                        updated_at=to_proto_timestamp(item.updated_at),
                    )
                    for item in order_with_items.items
                ]
            except OrderNotFoundError:
                await context.abort(grpc.StatusCode.NOT_FOUND, "ORDER_NOT_FOUND")

            return orders_pb2.OrderSummaryResponse(
                uuid=order_with_items.uuid,
                user_uuid=order_with_items.user_uuid,
                delivery_status=order_with_items.delivery_status,
                total_amount=order_with_items.total_amount,
                created_at=to_proto_timestamp(order_with_items.created_at),
                updated_at=to_proto_timestamp(order_with_items.updated_at),
                order_items=order_items,
            )
