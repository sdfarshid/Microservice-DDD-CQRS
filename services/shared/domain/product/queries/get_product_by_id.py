from pydantic import BaseModel
from uuid import UUID


class GetProductByIdQuery(BaseModel):
    product_id: UUID
