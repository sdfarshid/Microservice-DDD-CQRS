from pydantic import BaseModel
from app.domain.mixins.pagination import PaginationParams


class ListProductsQuery(BaseModel):
    pagination: PaginationParams
