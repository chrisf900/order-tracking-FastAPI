from abc import ABC, abstractmethod
from typing import List

from src.application.dtos.orders_dto import ItemDTO


class IPricingGateway(ABC):

    @abstractmethod
    async def calculate_total(self, items: List[ItemDTO]) -> float:
        pass
