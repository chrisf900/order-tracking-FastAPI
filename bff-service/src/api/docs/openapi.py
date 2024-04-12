from typing import Any, Dict

ORDER_RESPONSES: Dict[int | str, Dict[str, Any]] = {
    404: {"description": "Order not found"},
    400: {"description": "Validation error"},
    409: {"description": "Conflict when changing order status"},
    500: {"description": "Internal server error"},
}
