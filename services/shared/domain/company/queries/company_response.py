from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    provider_id: UUID
    registration_number: Optional[str]
    address: Optional[str]
    website: Optional[str]
    status: Optional[str]
    created_at: datetime | None = None
    updated_at: datetime | None = None
