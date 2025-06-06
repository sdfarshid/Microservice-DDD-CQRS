from pydantic import BaseModel
from uuid import UUID


class DeleteProductCommand(BaseModel):
    catalog_id: UUID
