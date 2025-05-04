from sqlalchemy import Column, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import Relationship

from app.domain.order.enums.item_status import ItemStatus
from app.infrastructure.database.mixins.audit_mixin import AuditMixin
from app.infrastructure.database.session import Base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class OrderItemDBModel(Base, AuditMixin):
    __tablename__ = 'order_items'
    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    order_id = Column(PG_UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Float, nullable=False)
    status = Column(Enum(ItemStatus, name='item_status'), nullable=False, default=ItemStatus.PENDING.value)

    order = Relationship("OrderDBModel", back_populates="items", lazy="select")