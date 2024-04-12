from abc import ABC, abstractmethod
from typing import Optional

from src.application.dtos.order_dto import OrderDTO
from src.domain.entities.order import OrderEntity


class IOrderRepository(ABC):

    @abstractmethod
    async def create_order(self, user_uuid: str, total_amount: float) -> OrderDTO:
        pass

    @abstractmethod
    async def get_order_by_uuid(self, order_uuid: str) -> Optional[OrderDTO]:
        pass

    @abstractmethod
    async def update_order_status(self, order_uuid: str, new_status: str) -> None:
        pass

    @abstractmethod
    async def update_total_order_amount(
        self, order_uuid: str, total_amount: float
    ) -> Optional[OrderEntity]:
        pass
