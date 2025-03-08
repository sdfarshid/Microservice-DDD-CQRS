from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserRole(BaseModel):
    id: UUID
    user_id: UUID
    role_id: UUID
