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

    async def create_product(self, command: CreateProductCommand):
        await self.__get_company_data(command.company_id)
        return await self.product_handler.create(command.to_domain_product())

    async def list_products(self, query: ListProductsQuery) -> list[ProductResponse]:
        listOfProductsDomainModel = await self.product_handler.list(query)
        return [ProductMapper.to_response(product) for product in listOfProductsDomainModel]

    async def get_product(self, query: GetProductByIdQuery) -> [ProductResponse, None]:
        productDomainModel = await self.product_handler.get(query)
        return ProductMapper.to_response(productDomainModel)

    async def delete_product(self, command: DeleteProductCommand) -> bool:
        return await self.product_handler.delete(command)

    async def update_product(self, command: UpdateProductCommand) -> [ProductResponse, None]:
        query = GetProductByIdQuery(product_id=command.product_id)
        product = await self.product_handler.get(query)
        if not product:
            raise ValueError("Product not found")
        if command.company_id is not None and product.company_id != command.company_id:
            await self.__get_company_data(command.company_id)

        updated_product = command.to_update_dict(command.update_from_command(product))
        DebugError(f"update_product : {updated_product}")
        productDomainModel = await self.product_handler.update((command.product_id, updated_product))
        DebugWaring(f"update_product : {type(productDomainModel)} : {productDomainModel}")
        return ProductMapper.to_response(productDomainModel)

    async def __get_company_data(self, company_id: UUID) -> [bool, dict]:
        res = await self._check_company_exists(company_id)
        DebugWaring(f"__get_company_data : {res}")
        if not res:
            DebugWaring(f"create_product : {res}")
            raise ValueError("Company not found")
        return res

    async def _check_company_exists(self, company_id: UUID) -> [bool, dict]:
        get_company_endpoint = f"{self.company_service_url}api/v1/company/{company_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(get_company_endpoint, timeout=10.0)
                response.raise_for_status()
                if response.status_code == 404:
                    DebugError(f"status_code404: {get_company_endpoint}")
                    return False
                elif response.status_code == 200:
                    DebugError(f"status_code200: {response} ")
                    return response.json()
        except httpx.RequestError as e:
            DebugError(f"HTTP error occurred: {e}")
            return False
        except httpx.HTTPStatusError as e:
            DebugError(f"HTTP status error occurred: {e}")
            return False
        except Exception as e:
            DebugError(f"Unexpected error occurred: {e}")
            return False
