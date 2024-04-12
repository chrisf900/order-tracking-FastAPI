from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.order_detail import OrderDetailEntity


class IOrderDetailRepository(ABC):
    @abstractmethod
    async def get_order_detail_by_order_uuid(
        self, order_uuid: str
    ) -> List[OrderDetailEntity]:
        raise NotImplementedError("IOrderDetailRepository method not implemented")

    @abstractmethod
    async def add_order_products(
        self, order_uuid: str, products: List[OrderDetailEntity]
    ) -> None:
        raise NotImplementedError("IOrderDetailRepository method not implemented")
