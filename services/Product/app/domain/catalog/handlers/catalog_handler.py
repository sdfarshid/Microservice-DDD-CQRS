from __future__ import annotations

from typing import List, Tuple, Sequence
from uuid import UUID
from fastapi import Depends
from app.domain.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.domain.catalog.models.catalog import Catalog
from app.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from app.domain.catalog.queries.get_catalog_by_name import GetCatalogByNameQuery
from app.domain.catalog.queries.get_catalogs_by_ids import GetCatalogsByIdsQuery
from app.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from app.infrastructure.repositories.catalog.catalog_repository import CatalogRepository
from app.infrastructure.repositories.catalog.interface.Irepository import IRepository
from shared.domain.product.commands.delete_product import DeleteProductCommand


class CatalogHandler(ICatalogHandler):
    def __init__(self, catalog_repository: IRepository = Depends(CatalogRepository)):
        self.catalog_repository = catalog_repository

    async def create(self, command: Catalog) -> Catalog:
        try:
            return await self.catalog_repository.add_catalog(command)
        except Exception as e:
            raise e

    async def find_by_name(self, query: GetCatalogByNameQuery) -> Catalog | None:
        return await self.catalog_repository.get_catalog_by_name(query.name)

    async def get(self, query: GetCatalogByIdQuery) -> Catalog | None:
        return await self.catalog_repository.get_catalog_by_id(query.catalog_id)

    async def list(self, query: ListCatalogsQuery) -> Sequence[Catalog]:
        return await self.catalog_repository.list_catalogs(query.pagination)

    async def delete(self, product_id: DeleteProductCommand) -> bool:
        return await self.catalog_repository.delete_catalog(product_id.catalog_id)

    async def update(self, command: Tuple[UUID, dict]) -> Catalog | None:
        product_id, updated_data = command
        return await self.catalog_repository.update_catalog(product_id, updated_data)

    async def get_by_ids(self, query: GetCatalogsByIdsQuery) -> List[Catalog]:
        return await self.catalog_repository.get_catalogs_by_ids(query.catalog_ids)
