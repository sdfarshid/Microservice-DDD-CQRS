from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UpdateProductCommand(BaseModel):
    product_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[str] = None

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.product_id})"
