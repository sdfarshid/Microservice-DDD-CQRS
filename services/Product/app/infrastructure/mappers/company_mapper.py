from app.domain.company.models.company import Company
from app.domain.company.models.value_objects.address import Address
from app.domain.company.models.value_objects.company_name import CompanyName
from app.domain.company.models.value_objects.registration_number import RegistrationNumber
from app.infrastructure.database.models.company import CompanyDBModel


class CompanyMapper():
    @staticmethod
    def to_domain(orm_model: CompanyDBModel) -> Company:
        return Company(
            id=orm_model.id,
            name=CompanyName(value=orm_model.name),
            provider_id=orm_model.provider_id,
            registration_number=RegistrationNumber(value=orm_model.registration_number),
            address=Address(value=orm_model.address),
            website=orm_model.website,
            status=orm_model.status,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )
    @staticmethod
    def to_orm(domain_model: Company) -> CompanyDBModel:
        return CompanyDBModel(
            id=domain_model.id,
            name=domain_model.name.value,
            provider_id=domain_model.provider_id,
            registration_number=domain_model.registration_number.value,
            address=domain_model.address.value,
            website=domain_model.website,
            status=domain_model.status,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at
        )