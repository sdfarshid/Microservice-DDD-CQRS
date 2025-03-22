from typing import List, Sequence
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.mixins.pagination import PaginationParams
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models.product import ProductDBModel
from app.infrastructure.repositories.product.interface.Icompany_repository import IProductRepository


class ProductRepository(IProductRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_product(self, product: ProductDBModel) -> ProductDBModel:
        try:
            self.db.add(product)
            await self.db.commit()
            await self.db.refresh(product)
            return product
        except IntegrityError as e:
            if "products_sku_key" in str(e):
                raise ValueError("SKU already exists. Please choose a different SKU.")
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_product_by_name(self, product_id: UUID) -> [ProductDBModel, None]:
        result = await self.db.execute(
            select(ProductDBModel).where(ProductDBModel.id == product_id)
        )
        return result.scalars().one_or_none()

    async def get_product_by_id(self, product_id: UUID) -> [ProductDBModel, None]:
        result = await self.db.execute(
            select(ProductDBModel).where(ProductDBModel.id == product_id)
        )
        return result.scalars().one_or_none()

    async def list_products(self, pagination: PaginationParams, company_id: [UUID, None]) -> Sequence[ProductDBModel]:
        query = select(ProductDBModel)
        if company_id:
            query = query.where(ProductDBModel.company_id == company_id)

        query = query.offset(pagination.offset).limit(pagination.limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_product(self, product_id: UUID, updated_data: dict) -> [ProductDBModel, None]:
        try:
            result = await self.db.execute(
                update(ProductDBModel)
                .where(ProductDBModel.id == product_id)
                .values(**updated_data)
                .returning(ProductDBModel)
            )
            await self.db.commit()
            return result.scalars().one_or_none()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            result = await self.db.execute(
                delete(ProductDBModel).where(ProductDBModel.id == product_id)
            )
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            raise e
