from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, List
from uuid import UUID

from app.infrastructure.database.models.catalog_products import CatalogProductDBModel


class IAssignRepository(ABC):
    @abstractmethod
    async def add_product_to_catalogs(self, product_id: UUID, catalog_ids: List[UUID]) -> bool:
        pass

    @abstractmethod
    async def update_product_catalogs(self, product_id: UUID, catalog_ids: List[UUID]) -> bool:
        pass

    @abstractmethod
    async def get_product_catalogs(self, product_id: UUID) -> List[CatalogProductDBModel]:
        pass
