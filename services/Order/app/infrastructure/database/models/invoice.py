from sqlalchemy import Column, String, DateTime, Float, Integer, UUID, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.domain.order.enums.invoice_status import InvoiceStatus
from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base


class InvoiceDBModel(Base, AuditMixin):
    __tablename__ = 'invoices'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    order_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    items_total = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(InvoiceStatus, name='invoice_status'), nullable=False, default=InvoiceStatus.PENDING.value)

    def __str__(self):
        return f"Invoice {self.id}"
