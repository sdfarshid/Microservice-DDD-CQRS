from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence, List
from uuid import UUID

from app.domain.order.aggregates.order import Order
from app.domain.order.entities.invoice import Invoice
from app.domain.order.entities.order_item import OrderItem
from app.infrastructure.database.models.invoice import InvoiceDBModel
from app.infrastructure.database.models.order import OrderDBModel
from app.infrastructure.database.models.order_item import OrderItemDBModel


class IOrderRepository(ABC):

    @abstractmethod
    async def add_invoice(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    async def add_order(self, orderAggregate: Order) -> Order:
        pass

    @abstractmethod
    async def get_invoice_by_id(self, invoice_id: UUID) -> Invoice | None:
        pass

    @abstractmethod
    async def update_invoice_status(self, invoice_id: UUID, status: str) -> bool:
        pass

    @abstractmethod
    async def get_expired_pending_invoices(self) -> List[Invoice]:
        pass
    @abstractmethod
    async def add_order_items_batch(self, order_items: List[OrderItemDBModel]) -> None:
        pass

    @abstractmethod
    async def update_order_item(self, item_id: UUID, status: str) -> OrderItem | None:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: UUID, status: str) -> bool:
        pass

    @abstractmethod
    async def update_order_items_status(self, order_id: UUID, status: str) -> bool:
        pass

    @abstractmethod
    async def get_orders_by_ids(self, order_id: UUID) -> Order | None:
        pass