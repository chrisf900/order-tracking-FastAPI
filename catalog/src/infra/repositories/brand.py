from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.brand import BrandEntity
from src.domain.ports.brand_repository import IBrandRepository
from src.infra.db.models.brand import Brand


class BrandRepository(IBrandRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_brands_by_uuid(self, brand_uuids: List[str]) -> List[BrandEntity]:
        query = select(Brand).where(Brand.uuid.in_(brand_uuids))
        result = await self.session.execute(query)

        brands = result.scalars().all()

        return [
            BrandEntity(
                uuid=brand.uuid,
                name=brand.name,
            )
            for brand in brands
        ]
