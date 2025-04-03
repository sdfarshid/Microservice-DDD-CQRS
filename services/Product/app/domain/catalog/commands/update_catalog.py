from datetime import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from app.domain.catalog.models.catalog import Catalog
from app.domain.catalog.models.value_objects.catalog_name import CatalogName


class UpdateCatalogCommand(BaseModel):
    catalog_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.catalog_id})"

    def update_from_command(self, catalog: Catalog) -> Catalog:
        return Catalog(
            id=catalog.id,
            name=CatalogName(value=self.name) if self.name else catalog.name,
            description=self.description if self.description else catalog.description,
            created_at=catalog.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def to_update_dict(catalog: Catalog) -> dict:
        return {
            "id": catalog.id,
            "name": catalog.name.value,
            "description": catalog.description,
            "created_at": catalog.created_at,
            "updated_at": catalog.updated_at
        }
