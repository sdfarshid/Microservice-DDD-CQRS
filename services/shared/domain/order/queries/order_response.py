from __future__ import annotations
from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: UUID
    quantity: int
    price: float
    name: str
    subtotal: float


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[OrderItemResponse]
    total: float
    status: str
    created_at: datetime
    updated_at: datetime | None = None
