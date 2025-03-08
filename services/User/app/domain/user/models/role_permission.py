from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class RolePermission(BaseModel):
    id: UUID
    role_id: UUID
    permission_id: UUID
