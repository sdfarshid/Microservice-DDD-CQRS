from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel

from app.domain.product.models.product import Product
from app.domain.product.models.value_objects.price import Price
from app.domain.product.models.value_objects.product_name import ProductName


class CreateProductCommand(BaseModel):
    name: str
    description: str | None = None
    price: float
    company_id: UUID
    stock: int
    status: str

    def to_domain_product(self) -> Product:
        return Product(
            name=ProductName(value=self.name),
            description=self.description,
            price=Price(value=self.price),
            company_id=self.company_id,
            stock=self.stock,
            status=self.status
        )
