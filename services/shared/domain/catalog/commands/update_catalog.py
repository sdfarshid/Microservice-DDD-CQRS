from datetime import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UpdateCatalogRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateCatalogCommand(UpdateCatalogRequest):
    catalog_id: UUID

    def __str__(self):
        return f"UpdateCompanyCommand(name={self.name}, id={self.catalog_id})"
