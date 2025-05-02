from __future__ import annotations

from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from app.application.mixins.audit_mixin import AuditMixin
from app.domain.order.entities.order_item import OrderItem
from app.domain.order.enums.order_status import OrderStatus


class Order(BaseModel, AuditMixin):
    id: UUID = uuid4()
    user_id: UUID
    items: List[OrderItem] = Field(default_factory=list)
    invoice_id: UUID
    status: OrderStatus = OrderStatus.PENDING

    def get_total_item(self) -> int:
        return sum([item.quantity for item in self.items])

    def get_total_amount(self) -> float:
        return  sum(item.quantity * item.price_at_order for item in self.items)


    def confirm(self):
        self.status = OrderStatus.CONFIRMED

    def cancel(self):
        self.status = OrderStatus.CANCELLED
