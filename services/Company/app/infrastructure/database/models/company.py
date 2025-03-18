
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base


class CompanyDBModel(Base, AuditMixin):
    __tablename__ = 'companies'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    provider_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    registration_number = Column(String(255), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    website = Column(String(255), nullable=True)
    status = Column(Enum('active', 'inactive', name='company_status'), nullable=False)

    def __str__(self):
        return f"Company(name={self.name}, id={self.id})"