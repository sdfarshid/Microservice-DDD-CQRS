from __future__ import annotations

from sqlite3 import IntegrityError
from typing import List, Sequence, Any, Coroutine
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.catalog.aggregates.catalog import Catalog
from app.domain.catalog.interface.Irepository import IRepository
from app.infrastructure.database.models.catalog import CatalogDBModel
from app.infrastructure.database.models.catalog_products import CatalogProductDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.mappers.catalog_mapper import CatalogMapper
from app.utilities.log import DebugError
from shared.mixins import PaginationParams


def _to_db_model(catalog: Catalog) -> CatalogDBModel:
    """Convert domain entity to database model"""
    return CatalogMapper.to_orm(catalog)


def _to_domain(db_model: CatalogDBModel) -> Catalog:
    """Convert database model to domain entity"""
    return CatalogMapper.to_domain(db_model)


class CatalogRepository(IRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def save(self, catalog: Catalog) -> Catalog:
        try:
            db_catalog = _to_db_model(catalog)
            merged_company = await self.db.merge(db_catalog)
            await self.db.commit()
            await self.db.refresh(merged_company)
            return _to_domain(merged_company)
        except IntegrityError as e:
            await self.db.rollback()
            DebugError(f"Integrity error in save: {e}")
            raise ValueError(f"Failed to save company: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            DebugError(f"Unexpected error in save: {e}")
            raise

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
        try:
            result = await self.db.execute(
                select(CatalogDBModel).offset(pagination.offset).limit(pagination.limit)
            )
            catalogs_db = result.scalars().all()
            if catalogs_db is None:
                return None

            return [_to_domain(catalog) for catalog in catalogs_db]
        except Exception as e:
            raise e

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

    async def get_catalogs_by_ids(self, catalog_ids: List[UUID]) -> List[Catalog]:
        result = await self.db.execute(
            select(CatalogDBModel).where(CatalogDBModel.id.in_(catalog_ids))
        )
        catalogs_db = result.scalars().all()
        return [CatalogMapper.to_domain(catalog_db) for catalog_db in catalogs_db]
