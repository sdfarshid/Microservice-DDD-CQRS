from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.product.aggregates.product import Product
from app.domain.product.value_objects.price import Price
from app.domain.product.value_objects.product_name import ProductName
from app.domain.product.value_objects.sku import SKU
from app.infrastructure.database.models.product import ProductDBModel


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


class ProductMapper:

    @staticmethod
    def to_domain(orm_model: ProductDBModel) -> Product:
        return Product(
            id=orm_model.id,
            name=ProductName(value=orm_model.name),
            description=orm_model.description,
            price=Price(value=orm_model.price),
            company_id=orm_model.company_id,
            sku=SKU(value=orm_model.sku),
            stock=orm_model.stock,
            reserved_stock=orm_model.reserved_stock,
            status=orm_model.status,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )

    @staticmethod
    def to_orm(domain_model: Product) -> ProductDBModel:
        return ProductDBModel(
            id=domain_model.id,
            name=domain_model.name.value,
            description=domain_model.description,
            price=domain_model.price.value,
            company_id=domain_model.company_id,
            stock=domain_model.stock,
            sku=domain_model.sku.value,
            status=domain_model.status,
            reserved_stock=domain_model.reserved_stock,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at
        )

    @staticmethod
    def to_response(domain_model: Product) -> ProductResponse:
        return ProductResponse(
            id=domain_model.id,
            name=domain_model.name.value,
            company_id=domain_model.company_id,
            sku=domain_model.sku.value,
            price=domain_model.price.value,
            reserved_stock=domain_model.reserved_stock,
            description=domain_model.description,
            stock=domain_model.stock,
            status=domain_model.status,
        )

    @staticmethod
    def to_db_dict(product: Product) -> dict:
        return {
            "id": product.id,
            "name": product.name.value,
            "description": product.description,
            "price": product.price.value,
            "company_id": product.company_id,
            "stock": product.stock,
            "sku": product.sku.value,
            "status": product.status,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "reserved_stock": product.reserved_stock
        }