from typing import List, Sequence
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.mixins.pagination import PaginationParams
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models.product import ProductDBModel


class ProductRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_product(self, product: ProductDBModel) -> ProductDBModel:
        try:
            self.db.add(product)
            await self.db.commit()
            await self.db.refresh(product)
            return product
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_product_by_id(self, product_id: UUID) -> [ProductDBModel, None]:
        result = await self.db.execute(
            select(ProductDBModel).where(ProductDBModel.id == product_id)
        )
        return result.scalars().one_or_none()

    async def list_products(self, pagination: PaginationParams) -> Sequence[ProductDBModel]:
        result = await self.db.execute(
            select(ProductDBModel).offset(pagination.offset).limit(pagination.limit)
        )
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
