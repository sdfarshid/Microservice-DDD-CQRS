from datetime import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from app.domain.company.models.company import Company
from app.domain.company.models.value_objects.address import Address
from app.domain.company.models.value_objects.company_name import CompanyName
from app.domain.company.models.value_objects.registration_number import RegistrationNumber
from app.infrastructure.database.models.company import CompanyDBModel


class UpdateCompanyCommand(BaseModel):
    company_id: UUID
    name: Optional[str] = None
    registration_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    status: Optional[str] = None

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.company_id})"

    def update_to_company(self, company: Company) -> Company:
        return Company(
            id=company.id,
            name=CompanyName(value=self.name) if self.name else company.name,
            provider_id=company.provider_id,
            registration_number=RegistrationNumber(
                value=self.registration_number) if self.registration_number else company.registration_number,
            address=Address(value=self.address) if self.address else company.address,
            website=self.website if self.website else company.website,
            status=self.status if self.status else company.status,
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
