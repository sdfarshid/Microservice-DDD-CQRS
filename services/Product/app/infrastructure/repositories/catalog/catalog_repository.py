from __future__ import annotations

from typing import List, Sequence
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.catalog.mixins.pagination import PaginationParams
from app.domain.catalog.models.catalog import Catalog
from app.infrastructure.database.models.catalog import CatalogDBModel
from app.infrastructure.database.models.catalog_products import CatalogProductDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.mappers.catalog_mapper import CatalogMapper
from app.infrastructure.repositories.catalog.interface.Irepository import IRepository


class CatalogRepository(IRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_catalog(self, catalog: Catalog) -> Catalog:
        try:
            catalog_db = CatalogMapper.to_orm(catalog)
            self.db.add(catalog_db)
            await self.db.commit()
            await self.db.refresh(catalog_db)
            return CatalogMapper.to_domain(catalog_db)
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_catalog_by_id(self, catalog_id: UUID) -> Catalog | None:
        result = await self.db.execute(
            select(CatalogDBModel).where(CatalogDBModel.id == catalog_id)
        )
        catalog_db = result.scalars().one_or_none()
        return CatalogMapper.to_domain(catalog_db) if catalog_db else None

    async def get_catalog_by_name(self, name: str) -> Catalog | None:
        result = await self.db.execute(
            select(CatalogDBModel).where(CatalogDBModel.name == name)
        )
        catalog_db = result.scalars().one_or_none()
        return CatalogMapper.to_domain(catalog_db) if catalog_db else None

    async def list_catalogs(self, pagination: PaginationParams) -> Sequence[Catalog]:
        result = await self.db.execute(
            select(CatalogDBModel).offset(pagination.offset).limit(pagination.limit)
        )
        catalogs_db = result.scalars().all()
        return [CatalogMapper.to_domain(catalog_db) for catalog_db in catalogs_db]

    async def update_catalog(self, catalog_id: UUID, updated_data: dict) -> Catalog | None:
        try:
            result = await self.db.execute(
                update(CatalogDBModel)
                .where(CatalogDBModel.id == catalog_id)
                .values(**updated_data)
                .returning(CatalogDBModel)
            )
            catalog_db = result.scalars().one_or_none()
            await self.db.commit()
            return CatalogMapper.to_domain(catalog_db) if catalog_db else None
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_catalog(self, catalog_id: UUID) -> bool:
        try:
            result = await self.db.execute(
                delete(CatalogDBModel).where(CatalogDBModel.id == catalog_id)
            )
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            raise e

    async def add_product_to_catalog(self, catalog_id: UUID, product_id: UUID) -> bool:
        try:
            catalog_product = CatalogProductDBModel(
                catalog_id=catalog_id,
                product_id=product_id
            )
            self.db.add(catalog_product)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            raise e
