from pydantic import BaseModel
from uuid import UUID


class DeleteProductCommand(BaseModel):
    product_id: UUID
