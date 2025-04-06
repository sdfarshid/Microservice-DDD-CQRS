from __future__ import annotations

from typing import List, Sequence
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.catalog_products import CatalogProductDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.catalog.interface.Iassign_repository import IAssignRepository
from app.utilities.log import DebugError


class AssignCatalogRepository(IAssignRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def _execute_transaction(self, operation):
        try:
            await operation()
            await self.db.commit()
            return True
        except Exception as e:
            DebugError(f"Error in _execute_transaction : {operation} {e}")
            await self.db.rollback()
            raise e

    async def _add_catalog_products(self, product_id: UUID, catalog_ids: List[UUID]) -> None:
        catalog_products = [
            CatalogProductDBModel(catalog_id=catalog_id, product_id=product_id)
            for catalog_id in catalog_ids
        ]
        self.db.add_all(catalog_products)

    async def add_product_to_catalogs(self, product_id: UUID, catalog_ids: List[UUID]) -> bool:
        async def operation():
            if catalog_ids:
                await self._add_catalog_products(product_id, catalog_ids)
        return await self._execute_transaction(operation)

    async def update_product_catalogs(self, product_id: UUID, catalog_ids: List[UUID]) -> bool:
        async def operation():
            await self.db.execute(
                delete(CatalogProductDBModel).where(CatalogProductDBModel.product_id == product_id)
            )
            if catalog_ids:
                await self._add_catalog_products(product_id, catalog_ids)

        return await self._execute_transaction(operation)

    async def get_product_catalogs(self, product_id: UUID) -> Sequence[CatalogProductDBModel]:
        try:
            result = await self.db.execute(
                select(CatalogProductDBModel).where(CatalogProductDBModel.product_id == product_id)
            )
            return result.scalars().all()
        except Exception as error:
            DebugError(f"Error in get_product_catalogs: {error}")
            raise error


