from __future__ import annotations
from typing import List
from uuid import UUID

from fastapi import Depends

from app.application.catalog.handlers.catalog_handler import CatalogHandler
from app.application.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.infrastructure.mappers.catalog_mapper import CatalogMapper
from app.utilities.log import DebugWaring, DebugError
from shared.domain.catalog.commands.delete_catalog import DeleteCatalogCommand
from shared.domain.catalog.commands.update_catalog import UpdateCatalogCommand, UpdateCatalogRequest
from shared.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from shared.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from shared.domain.catalog.queries.get_catalog_by_name import GetCatalogByNameQuery
from shared.domain.catalog.queries.catalog_response import CatalogResponse
from shared.domain.catalog.commands.create_catalog import CreateCatalogCommand


class CatalogService:
    def __init__(
            self,
            catalog_handler: ICatalogHandler = Depends(CatalogHandler),
    ):
        self.catalog_handler = catalog_handler

    async def create_catalog(self, command: CreateCatalogCommand) -> CatalogResponse:
        existing_catalog = await self.catalog_handler.find_by_name(GetCatalogByNameQuery(name=command.name))
        if existing_catalog:
            raise ValueError(f"Catalog with name {command.name} already exists - {existing_catalog.id}")
        catalog = await self.catalog_handler.create(command)
        return CatalogMapper.to_response(catalog)

    async def list_catalogs(self, query: ListCatalogsQuery) -> List[CatalogResponse]:
        DebugError(f"list_catalogs: {query}")
        catalogs = await self.catalog_handler.list(query)

        return [CatalogMapper.to_response(catalog) for catalog in catalogs]

    async def get_catalog(self, query: GetCatalogByIdQuery) -> CatalogResponse:
        catalog = await self.catalog_handler.get(query)
        if not catalog:
            raise ValueError(f"Catalog not found")
        return CatalogMapper.to_response(catalog)

    async def delete_catalog(self, command: DeleteCatalogCommand) -> bool:
        return await self.catalog_handler.delete(command)

    async def update_catalog(self, catalog_id: UUID, command: UpdateCatalogRequest) -> CatalogResponse | None:

        command = UpdateCatalogCommand(
            catalog_id=catalog_id,
            name=command.name,
            description=command.description)

        updated_catalog = await self.catalog_handler.update(command)

        return CatalogMapper.to_response(updated_catalog) if updated_catalog else None


