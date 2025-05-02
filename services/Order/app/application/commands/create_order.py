from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

from app.domain.order.entities.invoice import Invoice
from app.domain.order.aggregates.order import Order
from app.domain.order.entities.order_item import OrderItem
from app.domain.order.enums.invoice_status import InvoiceStatus
from app.domain.order.enums.order_status import OrderStatus
from app.domain.order.value_objects.price import Price


class OrderItemCommand(BaseModel):
    product_id: UUID
    quantity: int

    async def to_dict(self):
        return {"product_id": self.product_id, "quantity": self.quantity}


class CreateOrderCommand(BaseModel):
    user_id: UUID
    items: List[OrderItemCommand]

    #TODO:: add more features
    #shipping_address: str
    #discount_code: str | None = None

    def to_order_domain(self, invoice_id: UUID, items: List[OrderItem]) -> Order:
        return Order(
            id=uuid4(),
            user_id=self.user_id,
            invoice_id=invoice_id,
            items=items
        )


