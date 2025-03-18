from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.mixins.audit_mixin import AuditMixin
from app.domain.product.models.value_objects.price import Price
from app.domain.product.models.value_objects.product_name import ProductName


class Product(BaseModel, AuditMixin):
    id: UUID = uuid4()
    name: ProductName
    description: str | None = None
    price: Price
    company_id: UUID
    stock: int
    status: str
