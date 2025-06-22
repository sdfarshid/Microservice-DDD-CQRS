from __future__ import annotations
from pydantic import BaseModel


class CreateCatalogCommand(BaseModel):
    name: str
    description: str | None = None
