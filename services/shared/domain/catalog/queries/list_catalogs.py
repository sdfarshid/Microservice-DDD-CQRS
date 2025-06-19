from pydantic import BaseModel

from app.domain.catalog.mixins.pagination import PaginationParams


class ListCatalogsQuery(BaseModel):
    pagination: PaginationParams
