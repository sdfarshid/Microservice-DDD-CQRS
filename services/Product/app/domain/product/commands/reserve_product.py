from __future__ import annotations

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

class ReserveProductCommand(BaseModel):
    order_id: UUID
    items: List[dict[str, str | int]]  # [{"product_id": "uuid", "quantity": int}]

