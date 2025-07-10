from typing import List
from uuid import UUID
from fastapi import Depends

from app.application.handlers.order_handler import OrderHandler
from app.domain.order.aggregates.order import Order
from app.domain.order.entities.order_item import OrderItem
from shared.domain.order.commands.create_order import CreateOrderCommand
from shared.domain.order.enums.order_status import OrderStatus
from shared.domain.order.enums.item_status import ItemStatus
from app.utilities.log import DebugWarning, DebugError


class OrderService:
    def __init__(self, order_handler: OrderHandler, product_service, payment_service, invoice_service):
        self.handler = order_handler
        from app.application.order_saga import OrderCreationSaga
        self.saga = OrderCreationSaga(self, product_service, payment_service, invoice_service)

    async def create_order(self, command: CreateOrderCommand) -> dict:
        return await self.handle_order_creation(command)

    async def handle_order_creation(self, command: CreateOrderCommand) -> dict:
        return await self.saga.execute(command)

    # === Service Methods for Saga ===

    async def create_order_with_items(self, order: Order, items: List[OrderItem]) -> Order:
        DebugWarning(f"Creating order with {len(items)} items")
        created_order = await self.handler.create_order(order)
        await self.handler.add_order_items(order.id, items)
        return created_order

    async def mark_items_as_reserved(self, order_id: UUID, items: List[OrderItem]) -> None:
        """Mark all order items as reserved"""
        DebugWarning(f"Marking {len(items)} items as reserved for order {order_id}")
        for item in items:
            item.reserve()
            await self.handler.repository.update_order_item(item_id=item.id, status=item.status)

    async def confirm_order(self, order_id: UUID) -> Order:
        """Confirm an order by updating its status"""
        DebugWarning(f"Confirming order: {order_id}")
        order = await self.handler.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        order.confirm()
        return await self.handler.repository.save(order)

    async def cancel_order(self, order_id: UUID) -> Order:
        """Cancel an order and update its status"""
        DebugWarning(f"Cancelling order: {order_id}")
        order = await self.handler.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        order.cancel()
        return await self.handler.repository.save(order)

    async def complete_order(self, order_id: UUID) -> Order:
        """Complete an order after successful payment"""
        DebugWarning(f"Completing order: {order_id}")
        order = await self.handler.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        # Update order status to completed/shipped
        order.status = OrderStatus.SHIPPED
        return await self.handler.repository.save(order)

    async def get_order_by_id(self, order_id: UUID) -> Order:
        """Get order by ID"""
        return await self.handler.get_order_by_id(order_id)
