from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UpdateProductCommand(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    product_id: Optional[UUID] = None  # This will be set by the endpoint
    
    def __str__(self):
        return f"UpdateProductCommand(product_id={self.product_id})"
