from app.domain.catalog.aggregates.catalog import Catalog
from app.domain.catalog.value_objects.catalog_name import CatalogName
from app.infrastructure.database.models.catalog import CatalogDBModel
from shared.domain.catalog.queries.catalog_response import CatalogResponse


class CatalogMapper:

    @staticmethod
    def to_domain(orm_model: CatalogDBModel) -> Catalog:
        return Catalog(
            id=orm_model.id,
            name=CatalogName(value=orm_model.name),
            description=orm_model.description,
            created_at=orm_model.created_at
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

    def update_from_command(catalog: Catalog) -> Catalog:
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
