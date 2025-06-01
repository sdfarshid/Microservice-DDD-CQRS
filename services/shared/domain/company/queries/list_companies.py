from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from shared.mixins import PaginationParams


class ListCompaniesQuery(BaseModel):
    pagination: PaginationParams
    provider_id: Optional[UUID] = None

    def __str__(self):
        filter_info = f", provider_id={self.provider_id}" if self.provider_id else ""
        return f"ListCompaniesQuery(pagination={self.pagination}{filter_info})"
