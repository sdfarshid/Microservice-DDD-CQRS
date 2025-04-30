from sqlalchemy import Column, String, DateTime, Float, Integer, UUID, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.domain.order.enums.order_status import OrderStatus
from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base


class OrderDBModel(Base, AuditMixin):
    __tablename__ = 'orders'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    invoice_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    status = Column(Enum(OrderStatus, name='order_status'), nullable=False, default=OrderStatus.PENDING.value)

    def __str__(self):
        return f'Order {self.__dict__}'
