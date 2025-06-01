from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field


class CreateProductCommand(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    company_id: UUID
    status: str = Field(default="active")
    
    def __str__(self):
        return f"CreateProductCommand(name={self.name}, company_id={self.company_id})"
