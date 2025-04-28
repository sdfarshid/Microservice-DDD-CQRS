from typing import Dict, List
from uuid import UUID
from pydantic import BaseModel
class reserveItems(BaseModel):
    product_id: UUID
    quantity: int


class ReserveProductCommand(BaseModel):
    order_id: UUID
    items: List[reserveItems]  # [{"product_id": "uuid", "quantity": int}]

