from __future__ import annotations
from uuid import UUID, uuid4
from pydantic import BaseModel

from app.domain.product.value_objects.price import Price
from app.domain.product.value_objects.product_name import ProductName
from app.domain.product.value_objects.sku import SKU

from shared.domain.product.enums.product_status import ProductStatusEnum
from shared.mixins.audit_mixin import AuditMixin


class Product(BaseModel, AuditMixin):
    id: UUID = uuid4()
    name: ProductName
    sku: SKU
    description: str | None = None
    price: Price
    company_id: UUID
    reserved_stock: int = 0
    stock: int
    status: ProductStatusEnum

    def reserve_stock(self, quantity: int) -> None:
        if self.stock < quantity:
            raise ValueError("The quantity cannot be less than the reserved stock")
        self.stock -= quantity
        self.reserved_stock += quantity

    def release_stock(self, quantity: int) -> None:
        if self.reserved_stock <= 0:
            raise ValueError("The reserved stock is empty")
        self.stock += quantity
        self.reserved_stock -= quantity

    def update_name(self, new_name: ProductName) -> None:
        if new_name != self.name:
            self.name = new_name

    def update_description(self, new_description: str | None) -> None:
        if new_description != self.description:
            self.description = new_description

    def update_price(self, new_price: Price) -> None:
        if new_price != self.price:
            self.price = new_price

    def update_stock(self, new_stock: int) -> None:
        if new_stock != self.stock:
            self.stock = new_stock

    def update_sku(self, new_sku: SKU) -> None:
        if new_sku != self.sku:
            self.sku = new_sku

    def update_status(self, new_status: ProductStatusEnum) -> None:
        if new_status != self.status:
            self.status = new_status

