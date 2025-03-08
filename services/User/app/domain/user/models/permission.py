from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class Permission(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
