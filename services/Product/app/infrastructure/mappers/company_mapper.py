from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.commands.update_company import UpdateCompanyCommand
from app.domain.company.models.company import Company
from app.domain.company.models.value_objects.address import Address
from app.domain.company.models.value_objects.company_name import CompanyName
from app.domain.company.models.value_objects.registration_number import RegistrationNumber
from app.infrastructure.database.models.company import CompanyDBModel


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    provider_id: UUID
    registration_number: str
    address: str
    website: str | None = None
    status: str = "active"


class CompanyMapper():

    @staticmethod
    def convert_command_to_domain_model(command: CreateCompanyCommand) -> Company:
        return Company(
            name=CompanyName(value=command.name),
            provider_id=command.provider_id,
            registration_number=RegistrationNumber(value=command.registration_number),
            address=Address(value=command.address),
            website=command.website,
            status=command.status,
        )

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

    @staticmethod
    def to_response(domain_model: Company) -> CompanyResponse:
        return CompanyResponse(
            id=domain_model.id,
            name=domain_model.name.value,
            provider_id=domain_model.provider_id,
            registration_number=domain_model.registration_number.value,
            address=domain_model.address.value,
            website=domain_model.website,
            status=domain_model.status,
        )

    @staticmethod
    def update_from_command(company: Company, command: UpdateCompanyCommand) -> Company:
        return Company(
            id=company.id,
            name=CompanyName(value=command.name) if command.name is not None else company.name,
            provider_id=company.provider_id,
            registration_number=RegistrationNumber(value=command.registration_number) if command.registration_number is not None else company.registration_number,
            address=Address(value=command.address) if command.address is not None else company.address,
            website=command.website if command.website is not None else company.website,
            status=command.status if command.status is not None else company.status,
            created_at=company.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def to_update_dict(domain_model: Company) -> dict:
        return {
            "name": domain_model.name.value,
            "registration_number": domain_model.registration_number.value,
            "address": domain_model.address.value,
            "website": domain_model.website,
            "status": domain_model.status,
            "updated_at": datetime.now()
        }

