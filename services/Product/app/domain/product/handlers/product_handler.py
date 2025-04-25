from typing import List, Tuple, Optional
from uuid import UUID

from fastapi import Depends

from app.config.config import settings
from app.domain.product.commands.delete_product import DeleteProductCommand
from app.domain.product.handlers.interfaces.Iproduct_handler import IProductHandler
from app.domain.product.models.product import Product
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery
from app.domain.product.queries.get_product_by_ids import GetProductByIdsQuery
from app.domain.product.queries.list_products import ListProductsQuery
from app.infrastructure.mappers.product_mapper import ProductMapper
from app.infrastructure.repositories.product.interface.Irepository import IProductRepository
from app.infrastructure.repositories.product.product_repository import ProductRepository


class ProductHandler(IProductHandler):

    def __init__(self, product_repository: IProductRepository = Depends(ProductRepository)):
        self.repository = product_repository
        self.company_service_url = settings.COMPANY_SERVICE_URL

    async def create(self, command: Product) -> Product:
        try:
            product_db = ProductMapper.to_orm(command)
            await self.repository.add_product(product_db)
            return command
        except Exception as e:
            raise e

    async def get(self, query: GetProductByIdQuery) -> Optional[Product]:
        product_db = await self.repository.get_product_by_id(query.product_id)
        if not product_db:
            return None
        return ProductMapper.to_domain(product_db)

    async def list(self, query: ListProductsQuery) -> List[Product]:
        products_db = await self.repository.list_products(query.pagination, query.company_id)
        return [ProductMapper.to_domain(product) for product in products_db]

    async def delete(self, command: DeleteProductCommand) -> bool:
        return await self.repository.delete_product(command.product_id)

    async def update(self, command: Tuple[UUID, dict]) -> Product:
        product_id, updated_data = command
        product_db = await self.repository.update_product(product_id, updated_data)
        return ProductMapper.to_domain(product_db)

    async def get_batch_product_by_ids(self, query: GetProductByIdsQuery) -> List[Product]:
        products_db = await self.repository.get_products_by_ids(query.product_ids)
        return [ProductMapper.to_domain(product_db) for product_db in products_db]