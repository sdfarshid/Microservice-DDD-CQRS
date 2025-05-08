from pydantic import BaseModel
from app.domain.mixins.pagination import PaginationParams


class ListCompaniesQuery(BaseModel):
    pagination: PaginationParams

    def __str__(self):
        return f"ListCompaniesQuery(pagination={self.pagination})"