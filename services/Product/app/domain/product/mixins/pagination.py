from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PaginationParams(BaseModel):
    limit: int = 3
    offset: int = 0


async def get_pagination_params(limit: int = 3, offset: int = 0) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)

