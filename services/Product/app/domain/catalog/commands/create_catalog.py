from __future__ import annotations
from pydantic import BaseModel

from app.domain.catalog.models.catalog import Catalog
from app.domain.catalog.models.value_objects.catalog_name import CatalogName


class CreateCatalogCommand(BaseModel):
    name: str
    description: str | None = None

    def to_domain_catalog(self) -> Catalog:
        return Catalog(
            name=CatalogName(value=self.name),
            description=self.description
        )

