from sqlalchemy import Column, String, DateTime, UUID, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base


class CatalogDBModel(Base, AuditMixin):
    __tablename__ = 'catalogs'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
