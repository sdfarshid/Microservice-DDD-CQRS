from sqlalchemy import Column, String, DateTime, Float, Integer, UUID, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.database.session import Base
from datetime import datetime


class InvoiceDBModel(Base):
    __tablename__ = 'invoices'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum('FAILED', 'COMPLETED', 'PENDING', "CANCELLED", name='invoice_status'), nullable=False, default='PENDING')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return f"Invoice {self.id}"
