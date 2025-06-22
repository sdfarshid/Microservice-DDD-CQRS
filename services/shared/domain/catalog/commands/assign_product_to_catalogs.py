from __future__ import annotations

from typing import List
from uuid import UUID

from pydantic import BaseModel


class AssignProductToCatalogsCommand(BaseModel):
    product_id: UUID
    catalog_ids: List[UUID]


