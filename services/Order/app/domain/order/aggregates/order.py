from __future__ import annotations

from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from app.domain.order.entities.order_item import OrderItem

from shared.domain.order.enums.item_status import ItemStatus
from shared.domain.order.enums.order_status import OrderStatus
from shared.mixins.audit_mixin import AuditMixin


class Order(BaseModel, AuditMixin):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    items: List[OrderItem] = Field(default_factory=list)
    invoice_id: UUID
    status: OrderStatus = OrderStatus.PENDING

    @classmethod
    def create(cls, user_id: UUID, items: List[OrderItem], invoice_id: UUID,
               status: OrderStatus = OrderStatus.PENDING) -> Order:
        if not user_id:
            raise ValueError("User ID is required")
        if not invoice_id:
            raise ValueError("Invoice ID is required")
        if not items:
            raise ValueError("Order must have at least one item")
        return cls(user_id=user_id, items=items, invoice_id=invoice_id, status=status)

    def get_total_item(self) -> int:
        return sum([item.quantity for item in self.items])

    def get_total_amount(self) -> float:
        return sum(item.quantity * item.price_at_order for item in self.items)

    def reserve_items(self):
        for item in self.items:
            if item.status == ItemStatus.PENDING:
                item.status = ItemStatus.RESERVED

    def confirm(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError("This order is already confirmed")
        if not self.items:
            raise ValueError("there is no item in this order")
        self.status = OrderStatus.CONFIRMED

    def cancel(self):
        if self.status == OrderStatus.SHIPPED:
            raise ValueError("the order has already shipped")
        self.status = OrderStatus.CANCELLED
