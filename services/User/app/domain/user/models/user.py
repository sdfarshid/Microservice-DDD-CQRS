from pydantic import BaseModel, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.domain.user.value_objects import Email, Password

from shared.mixins.audit_mixin import AuditMixin


class UserResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class User(BaseModel, AuditMixin):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = uuid4()
    email: Email
    password: str
    is_active: bool = True

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    @classmethod
    def create(cls, email: Email, password: Password):
        return cls(
            email=email,
            password=password.value,
            is_active=True
        )
