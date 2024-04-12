from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.brand import BrandEntity


class IBrandRepository(ABC):
    @abstractmethod
    async def get_brands_by_uuid(self, brand_uuids: List[str]) -> List[BrandEntity]:
        raise NotImplementedError("IBrandRepository method not implemented")
