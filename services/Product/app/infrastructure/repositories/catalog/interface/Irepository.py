from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.catalog.models.catalog import Catalog
from app.domain.product.mixins.pagination import PaginationParams


class IRepository(ABC):

    @abstractmethod
    async def add_catalog(self, catalog: Catalog) -> Catalog:
        pass

    @abstractmethod
    async def list_catalogs(self, pagination: PaginationParams) -> Sequence[Catalog]:
        pass

    @abstractmethod
    async def get_catalog_by_id(self, catalog_id: UUID) -> Catalog | None:
        pass

    @abstractmethod
    async def get_catalog_by_name(self, name: str) -> Catalog | None:
        pass

    @abstractmethod
    async def update_catalog(self, catalog_id: UUID, updated_data: dict) -> Catalog | None:
        pass

    @abstractmethod
    async def delete_catalog(self, catalog_id: UUID) -> bool:
        pass

    @abstractmethod
    async def add_product_to_catalog(self, catalog_id: UUID, product_id: UUID) -> bool:
        pass
