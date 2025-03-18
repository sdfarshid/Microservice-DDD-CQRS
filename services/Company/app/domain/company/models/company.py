from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID, uuid4
from app.domain.company.models.value_objects.company_name import CompanyName
from app.domain.company.models.value_objects.address import Address
from app.domain.company.models.value_objects.registration_number import RegistrationNumber
from app.domain.mixins.audit_mixin import AuditMixin



class Company(BaseModel, AuditMixin):
    id: UUID = uuid4()
    name: CompanyName
    provider_id: UUID
    registration_number: RegistrationNumber
    address: Address
    website: str | None = None
    status: str = "active"
