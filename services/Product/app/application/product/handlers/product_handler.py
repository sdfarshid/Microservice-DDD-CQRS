from typing import List, Tuple, Optional
from uuid import UUID

from fastapi import Depends

from app.application.product.handlers.interfaces.Iproduct_handler import IProductHandler
from app.config.config import settings
from app.domain.product.aggregates.product import Product
from app.domain.product.interface.Irepository import IProductRepository
from app.infrastructure.mappers.product_mapper import ProductMapper
from app.infrastructure.repositories.product.product_repository import ProductRepository
from shared.domain.product.queries.GetProductByIdsQuery import GetProductByIdsQuery
from shared.domain.product.commands.delete_product import DeleteProductCommand
from shared.domain.product.queries.get_product_by_id import GetProductByIdQuery
from shared.domain.product.queries.list_products import ListProductsQuery


class ProductHandler(IProductHandler):

    def __init__(self, product_repository: IProductRepository = Depends(ProductRepository)):
        self.repository = product_repository

    async def create(self, command: Product) -> Product:
        try:
            await self.repository.add_product(command)
            return command
        except Exception as e:
            raise e

    async def get(self, query: GetProductByIdQuery) -> Optional[Product]:
        return await self.repository.get_product_by_id(query.product_id)

    async def list(self, query: ListProductsQuery) -> List[Product] | None:
        return await self.repository.list_products(query.pagination, query.company_id)

    async def delete(self, command: DeleteProductCommand) -> bool:
        return await self.repository.delete_product(command.product_id)

    async def update(self, command: Tuple[UUID, dict]) -> Product:
        product_id, updated_data = command
        product_db = await self.repository.update_product(product_id, updated_data)
        return ProductMapper.to_domain(product_db)

    async def get_batch_product_by_ids(self, query: GetProductByIdsQuery) -> List[Product]:
        products_db = await self.repository.get_products_by_ids(query.product_ids)
        return [ProductMapper.to_domain(product_db) for product_db in products_db]