from __future__ import annotations

from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.domain.catalog.models.catalog import Catalog
from app.domain.catalog.models.value_objects.catalog_name import CatalogName


class UpdateProductCatalogsCommand(BaseModel):
    product_id: UUID
    catalog_ids: List[UUID]