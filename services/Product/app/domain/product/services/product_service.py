from typing import List
from uuid import UUID

import httpx
from fastapi import Depends

from app.config.config import settings
from app.domain.product.commands.create_product import CreateProductCommand
from app.domain.product.commands.delete_product import DeleteProductCommand
from app.domain.product.commands.update_product import UpdateProductCommand
from app.domain.product.handlers.product_handler import ProductHandler
from app.domain.product.models.product import Product
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery
from app.domain.product.queries.list_products import ListProductsQuery
from app.infrastructure.mappers.product_mapper import ProductMapper, ProductResponse
from app.utilities.log import DebugWaring, DebugError


class ProductService:
    def __init__(
            self,
            product_handler: ProductHandler = Depends(ProductHandler),
    ):
        self.company_service_url = settings.COMPANY_SERVICE_URL
        self.product_handler = product_handler

    async def create_product(self, command: CreateProductCommand) -> Product:
        res = await self._check_company_exists(command.company_id)
        if not res:
            DebugWaring(f"create_product : {res}")
            raise ValueError("Company not found")

        return await self.product_handler.create(command.to_domain_product())

    async def list_products(self, query: ListProductsQuery) -> list[ProductResponse]:
        listOfProductsDomainModel = await self.product_handler.list(query)
        return [ProductMapper.to_response(product) for product in listOfProductsDomainModel]

    async def get_product(self, query: GetProductByIdQuery) -> [Product, None]:
        return await self.product_handler.get(query)

    async def delete_product(self, command: DeleteProductCommand) -> bool:
        return await self.product_handler.delete(command)

    async def update_product(self, command: UpdateProductCommand) -> [Product, None]:
        query = GetProductByIdQuery(product_id=command.product_id)
        product = await self.get_product(query)
        if not product:
            raise ValueError("Product not found")
        updated_product = ProductMapper.update_from_command(product, command)
        return await self.product_handler.update((command.product_id, updated_product))

    async def _check_company_exists(self, company_id: UUID) -> bool:
        try:
            DebugError(f"Checking company existence: {self.company_service_url}api/v1/company/{company_id}")
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.company_service_url}api/v1/company/{company_id}", timeout=10.0)
                response.raise_for_status()
                if response.status_code == 404:
                    DebugError(f"status_code404: {self.company_service_url}api/v1/company/{company_id}")
                    return False
                elif response.status_code == 200:
                    DebugError(f"status_code200: {self.company_service_url}api/v1/company/{company_id}")
                    return True
        except httpx.RequestError as e:
            DebugError(f"HTTP error occurred: {e}")
            return False
        except httpx.HTTPStatusError as e:
            DebugError(f"HTTP status error occurred: {e}")
            return False
        except Exception as e:
            DebugError(f"Unexpected error occurred: {e}")
            return False
