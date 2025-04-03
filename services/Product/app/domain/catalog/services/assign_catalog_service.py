from uuid import UUID

from fastapi import Depends

from app.domain.catalog.handlers.catalog_handler import CatalogHandler
from app.domain.catalog.handlers.interfaces.Icatalog_handler import ICatalogHandler
from app.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery


class AssignCatalogService:
    def __init__(
            self,
            catalog_handler: ICatalogHandler = Depends(CatalogHandler),
    ):
        self.catalog_handler = catalog_handler


    async def add_product_to_catalog(self, catalog_id: UUID, product_id: UUID) -> bool:
        catalog_query = GetCatalogByIdQuery(catalog_id=catalog_id)
        product_query = GetProductByIdQuery(product_id=product_id)
        catalog = await self.get_catalog(catalog_query)
        product = await self.get_product(product_query)
        if not catalog:
            raise ValueError("Catalog not found")
        if not product:
            raise ValueError("Product not found")
        return await self.catalog_handler.add_product_to_catalog(catalog_id, product_id)