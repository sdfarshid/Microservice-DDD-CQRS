from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UpdateCompanyRequest(BaseModel):
    name: Optional[str] = None
    registration_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    status: Optional[str] = None


class UpdateCompanyCommand(UpdateCompanyRequest):
    company_id: UUID

    class Config:
        json_encoders = {
            UUID: str
        }

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.company_id})"
