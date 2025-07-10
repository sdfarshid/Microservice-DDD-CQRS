from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.handlers import OrderHandler
from app.application.handlers.invoice_handler import InvoiceHandler
from app.domain.order.interface.IOrder_repository import IOrderRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.order_repository import OrderRepository


def get_repository(db: AsyncSession = Depends(get_db)) -> IOrderRepository:
    return OrderRepository(db=db)


def get_order_handler(
    repository: IOrderRepository = Depends(get_repository),
):
    return OrderHandler(
        repository=repository
    )


def get_invoice_handler(
    repository: IOrderRepository = Depends(get_repository),
):
    return InvoiceHandler(repository)
