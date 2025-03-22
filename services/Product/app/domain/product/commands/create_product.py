from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field

from app.domain.product.models.product import Product
from app.domain.product.models.value_objects.price import Price
from app.domain.product.models.value_objects.product_name import ProductName
from app.domain.product.models.value_objects.sku import SKU


class CreateProductCommand(BaseModel):
    name: str
    description: str | None = None
    price: float
    sku: str
    company_id: UUID
    stock: int
    status: str = Field(default="active")

    def to_domain_product(self) -> Product:
        return Product(
            name=ProductName(value=self.name),
            description=self.description,
            price=Price(value=self.price),
            sku=SKU(value=self.sku),
            company_id=self.company_id,
            stock=self.stock,
            status=self.status
        )
