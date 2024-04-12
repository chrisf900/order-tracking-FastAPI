from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.application.dtos.orders_dto import ItemDTO, OrderDetailDTO, OrderDTO


class IOrdersGateway(ABC):

    @abstractmethod
    async def get_order_by_uuid(self, order_uuid: UUID) -> OrderDTO:
        pass

    @abstractmethod
    async def create_order(
        self, user_uuid: UUID, total_amount: float, items: List[ItemDTO]
    ) -> OrderDTO:
        pass

    @abstractmethod
    async def update_order_status(self, order_uuid: UUID, status: str) -> OrderDTO:
        pass

    @abstractmethod
    async def cancel_order(self, order_uuid: UUID) -> OrderDTO:
        pass

    @abstractmethod
    async def get_order_summary_by_order_uuid(self, order_uuid: UUID) -> OrderDetailDTO:
        pass
