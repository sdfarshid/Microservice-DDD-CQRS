from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel


class CreateCompanyCommand(BaseModel):
    name: str
    provider_id: UUID
    registration_number: str
    address: str
    website: str | None = None
    status: str
