from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.category import CategoryEntity


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_categories_by_uuid(
        self, category_uuids: List[str]
    ) -> List[CategoryEntity]:
        raise NotImplementedError("ICategoryRepository method not implemented")
