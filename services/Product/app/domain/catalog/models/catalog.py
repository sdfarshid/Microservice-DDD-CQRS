from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.catalog.mixins.audit_mixin import AuditMixin
from app.domain.catalog.models.value_objects.catalog_name import CatalogName


class Catalog(BaseModel, AuditMixin):
    id: UUID = uuid4()
    name: CatalogName
    description: str | None = None
