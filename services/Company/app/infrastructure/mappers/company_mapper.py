from __future__ import annotations

import datetime

from app.domain import RegistrationNumber, CompanyName, Address, CompanyStatus
from app.domain.aggregates import Company
from shared import CreateCompanyCommand, CompanyResponse, UpdateCompanyCommand
from app.infrastructure.database.models.company import CompanyDBModel


class CompanyMapper:
    """Mapper to transform between domain models and DTOs"""

    @staticmethod
    def convert_command_to_domain_model(command: CreateCompanyCommand) -> Company:
        return Company(
            name=CompanyName(value=command.name),
            provider_id=command.provider_id,
            registration_number=RegistrationNumber(value=command.registration_number),
            address=Address(value=command.address),
            website=command.website,
            status=CompanyStatus(value=command.status),
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
            status=CompanyStatus(value=orm_model.status),
            created_at=orm_model.created_at or datetime.utcnow(),
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
            status=domain_model.status.value,
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
            status=domain_model.status.value,
        )

    def update_to_company(self, command: UpdateCompanyCommand, company: Company) -> Company:
        return Company(
            id=company.id,
            name=CompanyName(value=command.name) if command.name else company.name,
            provider_id=company.provider_id,
            registration_number=RegistrationNumber(
                value=command.registration_number) if command.registration_number else company.registration_number,
            address=Address(value=command.address) if command.address else company.address,
            website=command.website if command.website else company.website,
            status=CompanyStatus(value=command.status) if command.status else company.status,
            created_at=company.created_at
        )

    @staticmethod
    def to_update_dict(domain_model: Company) -> dict:
        return {
            "name": domain_model.name.value,
            "registration_number": domain_model.registration_number.value,
            "address": domain_model.address.value,
            "website": domain_model.website,
            "status": domain_model.status.value,
            "updated_at": domain_model.updated_at,
        }
