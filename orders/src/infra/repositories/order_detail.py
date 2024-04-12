import uuid
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.order_detail import OrderDetailEntity
from src.domain.exceptions import OrderDetailCreationError
from src.domain.repositories.order_detail_repository import IOrderDetailRepository
from src.infra.db.models.order_detail import OrderDetail


class OrderDetailRepository(IOrderDetailRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_detail_by_order_uuid(
        self, order_uuid: str
    ) -> List[OrderDetailEntity]:
        query = select(OrderDetail).where(OrderDetail.order_uuid == order_uuid)
        result = await self.session.execute(query)
        order_detail = result.scalars().all()

        return [
            OrderDetailEntity(
                uuid=str(item.uuid),
                order_uuid=str(item.order_uuid),
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in order_detail
        ]

    async def add_order_products(
        self, order_uuid: str, products: List[OrderDetailEntity]
    ) -> None:
        try:
            bulk_list = [
                {
                    "order_uuid": uuid.UUID(order_uuid),
                    "product_id": p.product_id,
                    "quantity": p.quantity,
                }
                for p in products
            ]

            if not bulk_list:
                raise OrderDetailCreationError("items not found")

            query = insert(OrderDetail).values(bulk_list)
            await self.session.execute(query)
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()
            # Loguear el error aquí
            raise OrderDetailCreationError(
                f"verify that the order {order_uuid} exists"
            ) from e
