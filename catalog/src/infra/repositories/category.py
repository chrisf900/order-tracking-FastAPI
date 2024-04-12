from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.category import CategoryEntity
from src.domain.ports.category_repository import ICategoryRepository
from src.infra.db.models.category import Category


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories_by_uuid(
        self, category_uuids: List[str]
    ) -> List[CategoryEntity]:
        query = select(Category).where(Category.uuid.in_(category_uuids))
        result = await self.session.execute(query)

        categories = result.scalars().all()

        return [
            CategoryEntity(
                uuid=category.uuid,
                name=category.name,
            )
            for category in categories
        ]
