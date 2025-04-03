from __future__ import annotations

from typing import List
from uuid import UUID

import httpx
from fastapi import Depends

from app.config.config import settings
from app.domain.catalog.commands.create_catalog import CreateCatalogCommand
from app.domain.catalog.commands.delete_catalog import DeleteCatalogCommand
from app.domain.catalog.commands.update_catalog import UpdateCatalogCommand
from app.domain.catalog.handlers.catalog_handler import CatalogHandler
from app.domain.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from app.domain.catalog.queries.get_catalog_by_name import GetCatalogByNameQuery
from app.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from app.infrastructure.mappers.catalog_mapper import CatalogMapper, CatalogResponse

from app.utilities.log import DebugWaring, DebugError


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
        catalog = await self.catalog_handler.create(command.to_domain_catalog())
        return CatalogMapper.to_response(catalog)

    async def list_catalogs(self, query: ListCatalogsQuery) -> List[CatalogResponse]:
        DebugError(f"list_catalogs: {query}")
        catalogs = await self.catalog_handler.list(query)
        return [CatalogMapper.to_response(catalog) for catalog in catalogs]

    async def get_catalog(self, query: GetCatalogByIdQuery) -> CatalogResponse | None:
        catalog = await self.catalog_handler.get(query)
        return CatalogMapper.to_response(catalog) if catalog else None

    async def delete_catalog(self, command: DeleteCatalogCommand) -> bool:
        return await self.catalog_handler.delete(command)

    async def update_catalog(self, command: UpdateCatalogCommand) -> CatalogResponse | None:
        query = GetCatalogByIdQuery(catalog_id=command.catalog_id)
        catalog = await self.catalog_handler.get(query)
        if not catalog:
            raise ValueError("Catalog not found")

        updated_data = command.to_update_dict(command.update_from_command(catalog))
        updated_catalog = await self.catalog_handler.update((command.catalog_id, updated_data))
        return CatalogMapper.to_response(updated_catalog) if updated_catalog else None


