from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CatalogResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
