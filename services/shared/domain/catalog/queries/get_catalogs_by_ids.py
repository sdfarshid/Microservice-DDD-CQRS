from typing import List
from uuid import UUID
from pydantic import BaseModel


class GetCatalogsByIdsQuery(BaseModel):
    catalog_ids: List[UUID]
