from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UpdateProductRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    status: Optional[str] = None


class UpdateProductCommand(UpdateProductRequest):
    product_id: UUID

    def __str__(self):
        return f"UpdateProductCommand({self.model_dump()})"
