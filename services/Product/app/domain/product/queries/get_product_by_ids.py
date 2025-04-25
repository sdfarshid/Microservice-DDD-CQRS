from pydantic import BaseModel
from uuid import UUID


class GetProductByIdsQuery(BaseModel):
    product_ids: list[UUID]
