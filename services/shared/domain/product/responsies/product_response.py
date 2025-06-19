from uuid import UUID

from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: UUID
    name: str
    company_id: UUID
    sku: str
    price: float
    description: str | None = None
    stock: int
    reserved_stock: int = 0
    status: str
