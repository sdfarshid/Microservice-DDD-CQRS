from __future__ import annotations
from typing import List, Tuple, Sequence
from uuid import UUID
from fastapi import Depends

from app.application.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.domain.catalog.aggregates.catalog import Catalog
from app.domain.catalog.interface.Irepository import IRepository
from app.domain.catalog.value_objects.catalog_name import CatalogName
from app.infrastructure.repositories.catalog.catalog_repository import CatalogRepository
from shared.domain.catalog.commands.create_catalog import CreateCatalogCommand
from shared.domain.catalog.commands.update_catalog import UpdateCatalogCommand
from shared.domain.catalog.queries.get_catalogs_by_ids import GetCatalogsByIdsQuery
from shared.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from shared.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from shared.domain.catalog.queries.get_catalog_by_name import GetCatalogByNameQuery
from shared.domain.product.commands.delete_product import DeleteProductCommand


class CatalogHandler(ICatalogHandler):
    def __init__(self, catalog_repository: IRepository = Depends(CatalogRepository)):
        self.catalog_repository = catalog_repository

    async def create(self, command: CreateCatalogCommand) -> Catalog:
        try:
            catalog = Catalog.create(CatalogName(value=command.name), command.description)
            return await self.catalog_repository.add_catalog(catalog)
        except Exception as e:
            raise e

    async def update(self, command: UpdateCatalogCommand) -> Catalog | None:
        catalog = await self.get(GetCatalogByIdQuery(catalog_id=command.catalog_id))
        if not catalog:
            raise ValueError("Catalog not found")

        if command.name is not None:
            command.name = CatalogName(value=command.name)

        catalog.update(name=command.name, description=command.description)
        return await self.catalog_repository.save(catalog)

    async def find_by_name(self, query: GetCatalogByNameQuery) -> Catalog | None:
        return await self.catalog_repository.get_catalog_by_name(query.name)

    async def get(self, query: GetCatalogByIdQuery) -> Catalog | None:
        return await self.catalog_repository.get_catalog_by_id(query.catalog_id)

    async def list(self, query: ListCatalogsQuery) -> Sequence[Catalog]:
        return await self.catalog_repository.list_catalogs(query.pagination)

    async def delete(self, product_id: DeleteProductCommand) -> bool:
        return await self.catalog_repository.delete_catalog(product_id.catalog_id)

    async def get_by_ids(self, query: GetCatalogsByIdsQuery) -> List[Catalog]:
        return await self.catalog_repository.get_catalogs_by_ids(query.catalog_ids)
