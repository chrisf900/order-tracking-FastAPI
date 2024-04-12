from typing import List

import grpc
from generated import orders_pb2, orders_pb2_grpc
from src.application.dtos.orders_dto import ItemDTO, OrderDetailDTO, OrderDTO
from src.application.ports.orders_gateway import IOrdersGateway
from src.infra.gateways.mappers.error_mapper import GrpcErrorTransformer


class OrdersGrpcGateway(IOrdersGateway):
    def __init__(self, channel: grpc.aio.Channel):
        self.stub = orders_pb2_grpc.OrderServiceStub(channel)

    async def get_order_by_uuid(self, order_uuid: str) -> OrderDTO:
        try:
            request = orders_pb2.OrderRequest(uuid=str(order_uuid))
            response = await self.stub.GetOrder(request)
        except grpc.RpcError as e:
            raise GrpcErrorTransformer.transform(e, entity="ORDER")

        return OrderDTO(
            uuid=response.uuid,
            user_uuid=response.user_uuid,
            delivery_status=response.delivery_status,
            total_amount=response.total_amount,
            created_at=response.created_at.ToDatetime(),
            updated_at=response.updated_at.ToDatetime(),
        )

    async def create_order(
        self, user_uuid: str, total_amount: float, items: List[ItemDTO]
    ) -> OrderDTO:
        try:
            order_items_request = [
                orders_pb2.OrderItemRequest(
                    uuid=item.uuid,
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
                for item in items
            ]

            request = orders_pb2.CreateOrderRequest(
                user_uuid=str(user_uuid),
                total_amount=total_amount,
                items=order_items_request,
            )

            response = await self.stub.CreateOrder(request)

        except grpc.RpcError as e:
            raise GrpcErrorTransformer.transform(e, entity="ORDER")

        return OrderDTO(
            uuid=response.uuid,
            user_uuid=response.user_uuid,
            delivery_status=response.delivery_status,
            total_amount=response.total_amount,
            created_at=response.created_at.ToDatetime(),
            updated_at=response.updated_at.ToDatetime(),
        )

    async def update_order_status(self, order_uuid: str, status: str) -> OrderDTO:
        try:
            request = orders_pb2.OrderStatusRequest(order_uuid=str(order_uuid), status=status)
            response = await self.stub.UpdateOrderStatus(request)
        except grpc.RpcError as e:
            raise GrpcErrorTransformer.transform(e, entity="ORDER")

        return OrderDTO(
            uuid=response.uuid,
            user_uuid=response.user_uuid,
            delivery_status=response.delivery_status,
            total_amount=response.total_amount,
            created_at=response.created_at.ToDatetime(),
            updated_at=response.updated_at.ToDatetime(),
        )

    async def cancel_order(self, order_uuid: str) -> OrderDTO:
        try:
            request = orders_pb2.OrderRequest(uuid=str(order_uuid))
            response = await self.stub.CancelOrder(request)
        except grpc.RpcError as e:
            raise GrpcErrorTransformer.transform(e, entity="ORDER")

        return OrderDTO(
            uuid=response.uuid,
            user_uuid=response.user_uuid,
            delivery_status=response.delivery_status,
            total_amount=response.total_amount,
            created_at=response.created_at.ToDatetime(),
            updated_at=response.updated_at.ToDatetime(),
        )

    async def get_order_summary_by_order_uuid(self, order_uuid: str) -> OrderDetailDTO:
        try:
            request = orders_pb2.OrderRequest(uuid=str(order_uuid))
            response = await self.stub.GetOrderSummary(request)
        except grpc.RpcError as e:
            raise GrpcErrorTransformer.transform(e, entity="ORDER")

        items = [
            ItemDTO(
                uuid=item.uuid,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            for item in response.order_items
        ]

        return OrderDetailDTO(
            uuid=response.uuid,
            user_uuid=response.user_uuid,
            delivery_status=response.delivery_status,
            total_amount=response.total_amount,
            items=items,
            created_at=response.created_at.ToDatetime(),
            updated_at=response.updated_at.ToDatetime(),
        )
