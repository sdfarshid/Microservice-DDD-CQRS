from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Role(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
