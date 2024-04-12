import asyncio
import logging

import grpc
from generated import orders_pb2_grpc
from src.config.logging import set_logging
from src.config.settings import settings
from src.interfaces.grpc.order_service import OrderService

logger = logging.getLogger(__name__)
set_logging()


async def serve_grpc():
    server = grpc.aio.server()
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    await server.start()
    logger.info(f"gRPC server started on port {settings.GRPC_PORT}")
    await server.wait_for_termination()


async def main():
    grpc_server = asyncio.create_task(serve_grpc())
    await asyncio.gather(grpc_server)


if __name__ == "__main__":
    asyncio.run(main())
