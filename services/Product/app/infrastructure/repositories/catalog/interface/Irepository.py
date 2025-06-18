from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, List
from uuid import UUID

from app.domain.catalog.models.catalog import Catalog
from shared.mixins import PaginationParams


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
    async def get_catalogs_by_ids(self, catalog_ids: List[UUID]) -> List[Catalog]:
        pass
