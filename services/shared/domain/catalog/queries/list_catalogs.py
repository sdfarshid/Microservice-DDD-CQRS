from pydantic import BaseModel

from shared.mixins import PaginationParams


class ListCatalogsQuery(BaseModel):
    pagination: PaginationParams

    def __str__(self):
        return f"ListCatalogsQuery(pagination={self.pagination})"