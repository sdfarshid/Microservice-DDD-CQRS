from typing import List, Tuple
from uuid import UUID

from fastapi import Depends

from app.config.config import settings
from app.domain.product.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.product.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.product.commands.create_product import CreateProductCommand
from app.domain.product.commands.delete_product import DeleteProductCommand
from app.domain.product.models.product import Product
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery
from app.domain.product.queries.list_products import ListProductsQuery
from app.infrastructure.mappers.product_mapper import ProductMapper
from app.infrastructure.repositories.product.interface.Icompany_repository import IProductRepository
from app.infrastructure.repositories.product.product_repository import ProductRepository


class ProductHandler(ICommandHandler, IQueryHandler):
    def __init__(self, product_repository: IProductRepository = Depends(ProductRepository)):
        self.product_repository = product_repository
        self.company_service_url = settings.COMPANY_SERVICE_URL

    async def create(self, command: Product) -> Product:
        try:
            product_db = ProductMapper.to_orm(command)
            await self.product_repository.add_product(product_db)
            return command
        except Exception as e:
            raise e

    async def get(self, query: GetProductByIdQuery) -> [Product, None]:
        product_db = await self.product_repository.get_product_by_id(query.product_id)
        if not product_db:
            return None
        return ProductMapper.to_domain(product_db)

    async def list(self, query: ListProductsQuery) -> List[Product]:
        products_db = await self.product_repository.list_products(query.pagination, query.company_id)
        return [ProductMapper.to_domain(product) for product in products_db]

    async def delete(self, command: DeleteProductCommand) -> bool:
        return await self.product_repository.delete_product(command.product_id)

    async def update(self, command: Tuple[UUID, dict]) -> [Product, None]:
        product_id, updated_data = command
        product_db = await self.product_repository.update_product(product_id, updated_data)
        return ProductMapper.to_domain(product_db)

