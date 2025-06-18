from datetime import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from app.domain.product.aggregates.product import Product
from app.domain.product.value_objects.price import Price
from app.domain.product.value_objects.product_name import ProductName
from app.domain.product.value_objects.sku import SKU


class UpdateProductCommand(BaseModel):
    product_id: Optional[UUID] = None
    company_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    sku: Optional[str] = None
    status: Optional[str] = None

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.product_id})"

    def update_from_command(self, product: Product) -> Product:
        return Product(
            id=product.id,
            name=ProductName(value=self.name) if self.name else product.name,
            description=self.description if self.description else product.description,
            price=Price(value=self.price) if self.price else product.price,
            company_id=product.company_id,
            stock=self.stock if self.stock else product.stock,
            sku=SKU(value=self.sku) if self.sku else product.sku,
            status=self.status if self.status else product.status,
            created_at=product.created_at,
            updated_at=datetime.now()
        )