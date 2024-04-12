import asyncio
import logging

import grpc
from generated import pricing_pb2_grpc
from src.config.logging import set_logging
from src.config.settings import settings
from src.infra.container import create_pricing_service_grpc

logger = logging.getLogger(__name__)
set_logging()


async def serve_grpc():
    catalog_channel = grpc.aio.insecure_channel(settings.catalog_service_url)
    pricing_service_grpc = create_pricing_service_grpc(catalog_channel)

    try:
        server = grpc.aio.server()
        pricing_pb2_grpc.add_PricingServiceServicer_to_server(
            pricing_service_grpc, server
        )

        server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
        await server.start()
        logger.info(f"gRPC server started on port {settings.GRPC_PORT}")
        await server.wait_for_termination()
    finally:
        await catalog_channel.close()


async def main():
    grpc_server = asyncio.create_task(serve_grpc())
    await asyncio.gather(grpc_server)


if __name__ == "__main__":
    asyncio.run(main())
