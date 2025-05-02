from datetime import datetime, timedelta
from typing import Sequence, List, Any, Coroutine
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete, Row, RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.order.aggregates.order import Order
from app.domain.order.entities.invoice import Invoice

from app.config.config import settings
from app.infrastructure.database.models.invoice import InvoiceDBModel
from app.infrastructure.database.models.order import OrderDBModel
from app.infrastructure.database.models.order_item import OrderItemDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.infrastructure.repositories.interface.IOrder_repository import IOrderRepository
from app.utilities.log import DebugError, DebugWarning


class OrderRepository(IOrderRepository):


    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def _execute_transaction(self, operation):
        try:
            await operation()
            await self.db.commit()
            return True
        except Exception as e:
            DebugError(f"Error in _execute_transaction : {operation} {e}")
            await self.db.rollback()
            raise e

    async def add_invoice(self, invoice: Invoice) -> Invoice:
        invoice_db = OrderMapper.to_invoice_orm(invoice)
        async def operation():
            self.db.add(invoice_db)

        await self._execute_transaction(operation)
        await self.db.refresh(invoice_db)
        return OrderMapper.to_invoice_domain(invoice_db)

    async def add_order(self, orderAggregate: Order) -> Order:
        order_db = OrderMapper.to_order_orm(orderAggregate)
        async def operation():
            self.db.add(order_db)

        await self._execute_transaction(operation)
        await self.db.refresh(order_db)
        return orderAggregate

    async def get_invoice_by_id(self, invoice_id: UUID) -> InvoiceDBModel | None:
        result = await self.db.execute(
            select(InvoiceDBModel).where(InvoiceDBModel.id == invoice_id)
        )
        return result.scalars().one_or_none()

    async def update_invoice_status(self, invoice_id: UUID, status: str) -> bool:

        async def operation():
            await self.db.execute(
                update(InvoiceDBModel)
                .where(InvoiceDBModel.id == invoice_id)
                .values(status=status, updated_at=datetime.now())
                .returning(InvoiceDBModel)
            )

        return await self._execute_transaction(operation)

    async def update_order_item(self, item_id: UUID, status: str) -> [OrderItemDBModel, None]:
        async def operation():
            await self.db.execute(
                update(OrderItemDBModel)
                .where(OrderItemDBModel.id == item_id)
                .values(status=status, updated_at=datetime.now())
                .returning(OrderItemDBModel)
            )

        await self._execute_transaction(operation)
        return OrderItemDBModel


    async def get_expired_pending_invoices(self) -> Sequence[InvoiceDBModel]:
        threshold = datetime.now() - timedelta(seconds=settings.get_expired_time())
        result = await self.db.execute(
            select(InvoiceDBModel)
            .where(InvoiceDBModel.status == "pending")
            .where(InvoiceDBModel.created_at <= threshold)
        )
        return result.scalars().all()

    async def add_order_items_batch(self, order_items: List[OrderItemDBModel]) -> None:
        async def operation():
            for item in order_items:
                self.db.add(item)

        await self._execute_transaction(operation)
