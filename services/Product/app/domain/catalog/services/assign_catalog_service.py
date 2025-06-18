from http.client import HTTPException
from uuid import UUID

from fastapi import Depends

from app.application.product.services.product_service import ProductService
from app.domain.catalog.commands.assign_product_to_catalogs import AssignProductToCatalogsCommand
from app.domain.catalog.commands.update_product_catalogs import UpdateProductCatalogsCommand
from app.domain.catalog.handlers.assign_product_to_catalog_handler import AssignProductToCatalogHandler
from app.domain.catalog.handlers.catalog_handler import CatalogHandler
from app.domain.catalog.handlers.interfaces.IAssign_catalog_handler import IAssignCatalogHandler
from app.domain.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from app.domain.catalog.queries.get_catalogs_by_ids import GetCatalogsByIdsQuery
from shared.domain.product.queries.get_product_by_id import GetProductByIdQuery


class AssignCatalogService:
    def __init__(
            self,
            assign_catalog_handler: IAssignCatalogHandler = Depends(AssignProductToCatalogHandler),
            catalog_handler: ICatalogHandler = Depends(CatalogHandler),
            product_service: ProductService = Depends(ProductService),
    ):
        self.catalog_handler = catalog_handler
        self.assign_catalog_handler = assign_catalog_handler
        self.product_service = product_service

    async def add_product_to_catalog(self, command: AssignProductToCatalogsCommand) -> bool:

        await self._get_product(command.product_id)
        await self._checkValidCatalogs(command)

        success = True
        for catalog_id in command.catalog_ids:
            result = await self.assign_catalog_handler.assign_product_to_catalogs(command)
            success = success and result

        return success

    async def update_product_catalogs(self, update_command: UpdateProductCatalogsCommand) -> bool:
        await self._get_product(update_command.product_id)
        return await self.assign_catalog_handler.update_product_catalogs(update_command)

    async def get_product_catalogs(self, query):
        data = await self.assign_catalog_handler.get_product_catalogs(query)
        if not data:
            raise HTTPException()
        return data

    async def _get_product(self, product_id: UUID):
        product_query = GetProductByIdQuery(product_id=product_id)
        product = await self.product_service.get_product(product_query)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

    async def _checkValidCatalogs(self, command):
        query = GetCatalogsByIdsQuery(catalog_ids=command.catalog_ids)
        catalogs = await self.catalog_handler.get_by_ids(query)
        found_catalog_ids = {catalog.id for catalog in catalogs}
        invalid_catalogs = set(command.catalog_ids) - found_catalog_ids

        if invalid_catalogs:
            raise ValueError(f"Catalogs with IDs {list(invalid_catalogs)} not found")
