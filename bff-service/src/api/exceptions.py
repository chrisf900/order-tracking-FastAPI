import logging

from fastapi import status
from fastapi.responses import JSONResponse
from requests import Request
from src.application.exceptions import BFFServiceError

logger = logging.getLogger(__name__)


def register_business_handlers(app):
    @app.exception_handler(BFFServiceError)
    async def handler(request: Request, exc: BFFServiceError):
        content = {
            "status_code": exc.status,
            "message": exc.message,
            "entity": exc.entity,
        }

        return JSONResponse(status_code=content.get("status_code"), content=content)

    @app.exception_handler(ValueError)
    async def key_error_handler(request: Request, exc: ValueError):
        content = {
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": str(exc),
        }
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)
