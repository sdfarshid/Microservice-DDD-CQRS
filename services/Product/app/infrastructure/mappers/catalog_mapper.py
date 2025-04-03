from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel

from app.domain.catalog.commands.create_catalog import CreateCatalogCommand
from app.domain.catalog.commands.update_catalog import UpdateCatalogCommand
from app.domain.catalog.models.catalog import Catalog
from app.domain.catalog.models.value_objects.catalog_name import CatalogName
from app.infrastructure.database.models.catalog import CatalogDBModel


class CatalogResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None


class CatalogMapper:
    @staticmethod
    def to_domain(orm_model: CatalogDBModel) -> Catalog:
        return Catalog(
            id=orm_model.id,
            name=CatalogName(value=orm_model.name),
            description=orm_model.description,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )

    @staticmethod
    def to_orm(domain_model: Catalog) -> CatalogDBModel:
        return CatalogDBModel(
            id=domain_model.id,
            name=domain_model.name.value,
            description=domain_model.description,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at
        )

    @staticmethod
    def to_response(domain_model: Catalog) -> CatalogResponse:
        return CatalogResponse(
            id=domain_model.id,
            name=domain_model.name.value,
            description=domain_model.description
        )
