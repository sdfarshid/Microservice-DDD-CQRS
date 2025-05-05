from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.product.mixins.audit_mixin import AuditMixin
from app.domain.product.value_objects.price import Price
from app.domain.product.value_objects.product_name import ProductName
from app.domain.product.value_objects.sku import SKU


class Product(BaseModel, AuditMixin):
    id: UUID = uuid4()
    name: ProductName
    sku: SKU
    description: str | None = None
    price: Price
    company_id: UUID
    reserved_stock: int = 0
    stock: int
    status: str

    def reserve_stock(self,quantity: int) -> None:
        if self.stock < quantity:
            raise ValueError("The quantity cannot be less than the reserved stock")
        self.stock -= quantity
        self.reserved_stock += quantity

    def release_stock(self,quantity: int) -> None:
        if self.reserved_stock <= 0 :
            raise ValueError("The reserved stock is empty")
        self.stock += quantity
        self.reserved_stock -= quantity

