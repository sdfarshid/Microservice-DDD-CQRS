from pydantic import BaseModel
from uuid import UUID


class DeleteCatalogCommand(BaseModel):
    catalog_id: UUID
