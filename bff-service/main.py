import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from src.api.dependencies import lifespan
from src.api.exceptions import register_business_handlers
from src.api.v1.routers import catalog, order
from src.config.logging import set_logging
from src.config.settings import settings

logger = logging.getLogger(__name__)
set_logging()


app = FastAPI(lifespan=lifespan)

register_business_handlers(app)

app.include_router(order.router, prefix="/market-api/v1/orders", tags=["Orders"])
app.include_router(catalog.router, prefix="/market-api/v1/catalog", tags=["Catalog"])


async def main():
    config = uvicorn.Config(
        app="main:app",
        host="0.0.0.0",
        port=settings.PORT,
        loop="asyncio",
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
