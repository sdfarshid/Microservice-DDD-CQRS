from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    quantity: int
    company_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime | None = None
