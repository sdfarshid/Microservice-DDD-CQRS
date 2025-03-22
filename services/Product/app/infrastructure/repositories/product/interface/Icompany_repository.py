from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.product.mixins.pagination import PaginationParams
from app.infrastructure.database.models.product import ProductDBModel


class IProductRepository(ABC):

    @abstractmethod
    async def add_product(self, product: ProductDBModel) -> ProductDBModel:
        pass

    @abstractmethod
    async def list_products(self, pagination: PaginationParams, company_id: [UUID, None]) -> Sequence[ProductDBModel]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: UUID) -> [ProductDBModel, None]:
        pass

    @abstractmethod
    async def update_product(self, product_id: UUID, updated_data: dict) -> [ProductDBModel, None]:
        pass

    @abstractmethod
    async def delete_product(self, product_id: UUID) -> bool:
        pass
    @abstractmethod
    async def get_product_by_name(self, product_id: UUID) -> [ProductDBModel, None]:
        pass
