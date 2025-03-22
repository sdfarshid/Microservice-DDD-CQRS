import uuid
from typing import Optional

from pydantic import BaseModel

from app.domain.product.mixins.pagination import PaginationParams


class ListProductsQuery(BaseModel):
    pagination: PaginationParams
    company_id: Optional[uuid.UUID] = None
