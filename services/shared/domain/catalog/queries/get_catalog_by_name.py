from pydantic import BaseModel
from uuid import UUID


class GetCatalogByNameQuery(BaseModel):
    name: str
