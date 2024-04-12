from abc import ABC, abstractmethod
from typing import List


class ICatalogGateway(ABC):

    @abstractmethod
    async def get_products(self, items: List[int]):
        raise NotImplementedError("ICatalogGateway method not implemented")
