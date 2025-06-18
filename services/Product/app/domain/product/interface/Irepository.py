from abc import ABC, abstractmethod
from typing import Sequence, Optional
from uuid import UUID

from app.domain.product.aggregates.product import Product
from app.infrastructure.database.models.product import ProductDBModel
from shared.mixins import PaginationParams


class IProductRepository(ABC):

    @abstractmethod
    async def add_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def list_products(self, pagination: PaginationParams, company_id: Optional[UUID]) -> list[Product] | None:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: UUID) -> Product | None:
        pass

    @abstractmethod
    async def get_products_by_ids(self, product_id: list[UUID]) -> list[Product]:
        pass

    @abstractmethod
    async def update_product(self, product_id: UUID, updated_data: dict) -> Product | None:
        pass

    @abstractmethod
    async def delete_product(self, product_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_product_by_name(self, product_id: UUID) -> Product | None:
        pass
