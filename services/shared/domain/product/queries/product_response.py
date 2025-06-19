from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.domain.product.value_objects.sku import SKU


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    quantity: int
    sku: str
    reserved_stock: int
    stock: int
    company_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime | None = None
