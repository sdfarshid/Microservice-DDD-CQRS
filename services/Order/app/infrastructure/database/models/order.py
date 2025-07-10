from sqlalchemy import Column, String, DateTime, Float, Integer, UUID, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Relationship

from shared.domain.order.enums.order_status import OrderStatus
from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base


class OrderDBModel(Base, AuditMixin):
    __tablename__ = 'orders'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    invoice_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    status = Column(Enum(OrderStatus, name='order_status'), nullable=False, default=OrderStatus.PENDING.value)

    items = Relationship("OrderItemDBModel", back_populates="order", lazy="select")
    invoice = Relationship("InvoiceDBModel", back_populates="order", uselist=False, lazy="select")

    def __str__(self):
        return f'Order {self.__dict__}'
