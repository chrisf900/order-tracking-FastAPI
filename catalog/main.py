import asyncio
import logging

import grpc
from generated import catalog_pb2_grpc
from src.config.logging import set_logging
from src.config.settings import settings
from src.interfaces.grpc.catalog_service import CatalogService

logger = logging.getLogger(__name__)
set_logging()


async def serve_grpc():
    server = grpc.aio.server()
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(CatalogService(), server)
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    await server.start()
    logger.info(f"gRPC server started on port {settings.GRPC_PORT}")
    await server.wait_for_termination()


async def main():
    grpc_server = asyncio.create_task(serve_grpc())
    await asyncio.gather(grpc_server)


if __name__ == "__main__":
    asyncio.run(main())
