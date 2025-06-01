from __future__ import annotations

from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from app.domain.value_objects.company_name import CompanyName
from app.domain.value_objects.registration_number import RegistrationNumber
from app.domain.value_objects.address import Address
from app.domain.value_objects.company_status import CompanyStatus
from shared import CompanyStatusEnum
from shared.mixins.audit_mixin import AuditMixin


class Company(BaseModel, AuditMixin):
    id: UUID = Field(default_factory=uuid4)
    name: CompanyName
    provider_id: UUID
    registration_number: RegistrationNumber
    address: Address
    website: str | None = None
    status: CompanyStatus = CompanyStatus(value=CompanyStatusEnum.ACTIVE)

    def create(self,
               name: CompanyName,
               provider_id: UUID,
               registration_number: RegistrationNumber,
               address: Address,
               website: str | None = None
               ) -> "Company":
        return clc(
            name=name,
            provider_id=provider_id,
            registration_number=registration_number,
            address=address,
            website=website,
            status=CompanyStatus(value=CompanyStatusEnum.ACTIVE)
        )

    def update_name(self, new_name: CompanyName):
        if new_name != self.name:
            self.name = new_name

    def update_address(self, new_address: Address):
        if new_address != self.address:
            self.address = new_address

    def update_website(self, new_website: str | None):
        if new_website != self.website:
            self.website = new_website

    def update_status(self, new_status: CompanyStatus):
        if new_status != self.status:
            self.status = new_status

    def update_registration_number(self, new_reg_number: RegistrationNumber):
        if new_reg_number != self.registration_number:
            self.registration_number = new_reg_number
