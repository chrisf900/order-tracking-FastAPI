import grpc
from fastapi import status
from src.application.exceptions import BFFServiceError


class GrpcErrorTransformer:
    _STATUS_MAP = {
        grpc.StatusCode.NOT_FOUND: (status.HTTP_404_NOT_FOUND, "RESOURCE_NOT_FOUND"),
        grpc.StatusCode.INVALID_ARGUMENT: (status.HTTP_400_BAD_REQUEST, "BAD_REQUEST"),
        grpc.StatusCode.ALREADY_EXISTS: (status.HTTP_409_CONFLICT, "DUPLICATE_ENTITY"),
        grpc.StatusCode.UNAUTHENTICATED: (status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED"),
        grpc.StatusCode.PERMISSION_DENIED: (status.HTTP_403_FORBIDDEN, "ACCESS_DENIED"),
        grpc.StatusCode.FAILED_PRECONDITION: (
            status.HTTP_409_CONFLICT,
            "FAILED_PRECONDITION",
        ),
        grpc.StatusCode.UNAVAILABLE: (
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "SERVICE_UNAVAILABLE",
        ),
        grpc.StatusCode.DEADLINE_EXCEEDED: (status.HTTP_504_GATEWAY_TIMEOUT, "TIMEOUT"),
    }

    @classmethod
    def transform(cls, e: grpc.RpcError, entity: str) -> BFFServiceError:
        grpc_status = e.code()
        grpc_details = e.details()

        http_status, internal_code = cls._STATUS_MAP.get(
            grpc_status,
            (status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR"),
        )

        return BFFServiceError(
            status=http_status, message=grpc_details, entity=entity.upper()
        )
