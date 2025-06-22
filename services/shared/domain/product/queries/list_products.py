import uuid
from typing import Optional

from pydantic import BaseModel

from shared.mixins import PaginationParams


class ListProductsQuery(BaseModel):
    pagination: PaginationParams
    company_id: Optional[uuid.UUID] = None

    def __str__(self):
        return f"ListProductsQuery(pagination={self.pagination})"
