from __future__ import annotations

from typing import List
from uuid import UUID
from pydantic import BaseModel


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
