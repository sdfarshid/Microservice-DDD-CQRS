from __future__ import annotations

from typing import List, Tuple, Sequence
from uuid import UUID
from fastapi import Depends

from app.domain.catalog.commands.assign_product_to_catalogs import AssignProductToCatalogsCommand
from app.domain.catalog.commands.update_product_catalogs import UpdateProductCatalogsCommand
from app.domain.catalog.handlers.interfaces.IAssign_catalog_handler import IAssignCatalogHandler, TCommand, TResult, \
    TQuery
from app.domain.catalog.queries.get_product_catalogs import GetProductCatalogsQuery
from app.infrastructure.repositories.catalog.assign_catalog_repository import AssignCatalogRepository
from app.infrastructure.repositories.catalog.interface.Iassign_repository import IAssignRepository
from app.utilities.log import DebugWaring


class AssignProductToCatalogHandler(IAssignCatalogHandler):

    def __init__(self, repository: IAssignRepository = Depends(AssignCatalogRepository)):
        self.repository = repository

    async def assign_product_to_catalogs(self, command: AssignProductToCatalogsCommand) -> bool:
        return await self.repository.add_product_to_catalogs(command.product_id, command.catalog_ids)

    async def update_product_catalogs(self, command: UpdateProductCatalogsCommand) -> bool:
        return await self.repository.update_product_catalogs(command.product_id, command.catalog_ids)

    async def get_product_catalogs(self, query: GetProductCatalogsQuery) -> List[UUID]:
        rows = await self.repository.get_product_catalogs(query.product_id)
        if not rows:
            raise ValueError("Product not found")
        return [row.catalog_id for row in rows]

