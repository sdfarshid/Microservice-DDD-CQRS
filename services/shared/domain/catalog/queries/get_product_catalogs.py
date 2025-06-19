from typing import List
from uuid import UUID

from pydantic import BaseModel


class GetProductCatalogsQuery(BaseModel):
    product_id: UUID

