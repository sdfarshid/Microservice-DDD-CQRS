from typing import List, Sequence, Optional, Any, Coroutine
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.aggregates.product import Product
from app.domain.product.interface.Irepository import IProductRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models.product import ProductDBModel
from app.infrastructure.mappers.product_mapper import ProductMapper
from shared.mixins import PaginationParams


class ProductRepository(IProductRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_product(self, product: Product) -> Product:
        try:
            product_db = ProductMapper.to_orm(product)

            self.db.add(product_db)
            await self.db.commit()
            await self.db.refresh(product_db)
            return product
        except IntegrityError as e:
            if "products_sku_key" in str(e):
                raise ValueError("SKU already exists. Please choose a different SKU.")
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_product_by_name(self, product_id: UUID) -> Product | None:
        result = await self.db.execute(
            select(ProductDBModel).where(ProductDBModel.id == product_id)
        )
        product_db = result.scalar().one_or_none()
        if not product_db:
            return None
        return ProductMapper.to_domain(product_db)

    async def get_product_by_id(self, product_id: UUID) -> Product | None:
        result = await self.db.execute(
            select(ProductDBModel).where(ProductDBModel.id == product_id)
        )
        product_db = result.scalars().one_or_none()
        if not product_db:
            return None
        return ProductMapper.to_domain(product_db)

    async def list_products(self, pagination: PaginationParams, company_id: [UUID, None]) -> list[Product] | None:
        query = select(ProductDBModel)
        if company_id:
            query = query.where(ProductDBModel.company_id == company_id)

        query = query.offset(pagination.offset).limit(pagination.limit)

        result = await self.db.execute(query)
        products_db = result.scalars().all()
        if products_db is None:
            return None

        return [ProductMapper.to_domain(product) for product in products_db]

    async def update_product(self, product_id: UUID, updated_data: dict) -> Product | None:
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

    async def get_products_by_ids(self, product_ids: List[UUID]) -> list[Product] | None:
        try:
            result = await self.db.execute(
                select(ProductDBModel).where(ProductDBModel.id.in_(product_ids))
            )
            return result.scalars().all()
        except Exception as e:
            raise e
