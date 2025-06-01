from __future__ import annotations

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field


class reserveItems(BaseModel):
    product_id: UUID
    quantity: int


class ReserveProductCommand(BaseModel):
    order_id: UUID
    items: List[reserveItems]  # [{"product_id": "uuid", "quantity": int}]

