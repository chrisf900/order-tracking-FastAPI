import datetime
import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.order import OrderEntity
from src.domain.exceptions import (
    OrderCreationError,
    OrderNotFoundError,
    OrderStatusNotUpdatedError,
)
from src.domain.repositories.order_repository import IOrderRepository
from src.infra.db.models.order import Order


class OrderRepository(IOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_uuid: str, total_amount: float) -> OrderEntity:
        try:
            order = Order(
                user_uuid=uuid.UUID(user_uuid),
                delivery_status="IN_PROGRESS",
                total_amount=total_amount,
            )
            self.session.add(order)
            await self.session.commit()
            await self.session.refresh(order)
        except IntegrityError as e:
            await self.session.rollback()
            raise OrderCreationError() from e

        return OrderEntity(
            uuid=str(order.uuid),
            user_uuid=str(order.user_uuid),
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    async def get_order_by_uuid(self, order_uuid: str) -> OrderEntity:
        query = select(Order).where(Order.uuid == order_uuid)
        result = await self.session.execute(query)
        order = result.scalars().first()

        if not order:
            raise OrderNotFoundError()

        return OrderEntity(
            uuid=str(order.uuid),
            user_uuid=str(order.user_uuid),
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    async def update_order_status(self, order_uuid: str, new_status: str) -> None:
        try:
            query = (
                update(Order)
                .where(Order.uuid == order_uuid)
                .values(
                    delivery_status=new_status,
                    updated_at=datetime.datetime.now(datetime.UTC),
                )
            )

            result = await self.session.execute(query)

            if result.rowcount == 0:
                raise OrderStatusNotUpdatedError(f"order {order_uuid} not updated")

            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise OrderStatusNotUpdatedError(
                f"verify that the order {order_uuid} exists"
            ) from e

    async def update_total_order_amount(
        self, order_uuid: str, total_amount: float
    ) -> Optional[OrderEntity]:

        query = await self.session.execute(
            select(Order).where(Order.uuid == order_uuid)
        )
        order = query.scalar_one_or_none()

        if not order:
            return None

        order.total_amount = total_amount
        order.updated_at = datetime.datetime.now(datetime.UTC)
        await self.session.commit()

        return OrderEntity(
            uuid=order.uuid,
            user_uuid=order.user_uuid,
            delivery_status=order.delivery_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
