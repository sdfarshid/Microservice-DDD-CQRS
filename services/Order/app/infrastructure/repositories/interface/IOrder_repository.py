from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence, List
from uuid import UUID

from app.infrastructure.database.models.invoice import InvoiceDBModel
from app.infrastructure.database.models.order import OrderDBModel
from app.infrastructure.database.models.order_item import OrderItemDBModel


class IOrderRepository(ABC):

    @abstractmethod
    async def add_invoice(self, invoice: InvoiceDBModel) -> InvoiceDBModel:
        pass

    @abstractmethod
    async def add_order(self, order: OrderDBModel) -> OrderDBModel:
        pass

    @abstractmethod
    async def get_invoice_by_id(self, invoice_id: UUID) -> [InvoiceDBModel, None]:
        pass

    @abstractmethod
    async def update_invoice_status(self, invoice_id: UUID, status: str) -> [InvoiceDBModel, None]:
        pass

    @abstractmethod
    async def get_expired_pending_invoices(self) -> Sequence[InvoiceDBModel]:
        pass
    @abstractmethod
    async def add_order_items_batch(self, order_items: List[OrderItemDBModel]) -> None:
        pass

    @abstractmethod
    async def update_order_item(self, item_id: UUID, status: str) -> [OrderItemDBModel, None]:
        pass
