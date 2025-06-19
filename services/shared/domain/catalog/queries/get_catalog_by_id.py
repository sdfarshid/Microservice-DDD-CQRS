from pydantic import BaseModel
from uuid import UUID


class GetCatalogByIdQuery(BaseModel):
    catalog_id: UUID
