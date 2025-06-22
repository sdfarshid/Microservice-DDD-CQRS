from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.domain.catalog.value_objects.catalog_name import CatalogName
from shared.mixins.audit_mixin import AuditMixin


class Catalog(BaseModel, AuditMixin):
    id: UUID = Field(default_factory=uuid4)
    name: CatalogName
    description: str | None = None

    @classmethod
    def create(cls, name: CatalogName, description: str | None = None) -> Catalog:
        if name is None:
            raise ValueError("Catalog name is required")
        return cls(name=name, description=description)

    def update(self, name: CatalogName | None = None, description: str | None = None):
        if name is not None:
            self.name = name

        self.description = description
        self.updated_at = datetime.now()
