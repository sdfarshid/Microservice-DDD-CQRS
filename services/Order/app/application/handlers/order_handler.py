import asyncio
import decimal
from typing import List
from uuid import UUID, uuid4

from fastapi import Depends

from app.application.order_saga import OrderCreationSaga
from app.domain.order.aggregates.order import Order
from app.domain.order.entities.invoice import Invoice
from app.domain.order.entities.order_item import OrderItem

from app.domain.order.interface.IOrder_repository import IOrderRepository
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.infrastructure.repositories.order_repository import OrderRepository
from app.utilities.gateway_client import GatewayClient
from app.utilities.log import DebugError, DebugWarning
from shared.domain.order.enums.order_status import OrderStatus
from shared.domain.order.enums.item_status import ItemStatus
from shared.domain.order.enums.invoice_status import InvoiceStatus
from shared.domain.order.commands.create_order import CreateOrderCommand, OrderItemCommand


class OrderHandler:
    def __init__(self, repository: IOrderRepository):
        self.repository = repository

    async def create_order(self, order: Order):
        return await self.repository.add_order(order)

    async def add_order_items(self, order_id: UUID, items: List[OrderItem]):
        return await self.repository.add_order_items_batch(order_id, items)

    async def update_order_status(self, order_id: UUID, status: OrderStatus):
        return await self.repository.update_order_status(order_id, status.value)

    async def get_order_by_id(self, order_id: UUID) -> Order:
        return await self.repository.get_orders_by_ids(order_id)

    async def cancel_order(self, order: Order):
        """Cancel an order and update its status"""
        order.cancel()
        await self.repository.save(order)
        await self.repository.update_invoice_status(order.invoice_id, InvoiceStatus.FAILED)

