from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.product.commands.create_product import CreateProductCommand
from app.domain.product.commands.update_product import UpdateProductCommand
from app.domain.product.models.product import Product
from app.domain.product.models.value_objects.price import Price
from app.domain.product.models.value_objects.product_name import ProductName
from app.domain.product.models.value_objects.sku import SKU
from app.infrastructure.database.models.product import ProductDBModel


class ProductResponse(BaseModel):
    id: UUID
    name: str
    company_id: UUID
    sku: str
    price: float
    description: str | None = None
    stock: int
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
            stock=domain_model.stock,
            status=domain_model.status,
        )


    @staticmethod
    def update_from_command(product: Product, command: UpdateProductCommand) -> Product:
        return Product(
            id=product.id,
            name=ProductName(value=command.name) if command.name is not None else product.name,
            description=command.description if command.description is not None else product.description,
            price=Price(value=command.price) if command.price is not None else product.price,
            company_id=product.company_id,
            stock=command.stock if command.stock is not None else product.stock,
            status=command.status if command.status is not None else product.status,
            created_at=product.created_at,
            updated_at=datetime.now()
        )
