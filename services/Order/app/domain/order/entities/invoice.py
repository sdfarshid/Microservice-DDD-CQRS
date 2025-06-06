from __future__ import annotations
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.application.mixins.audit_mixin import AuditMixin
from app.domain.order.enums.invoice_status import InvoiceStatus
from app.domain.order.value_objects.price import Price


class Invoice(BaseModel, AuditMixin):
    id: UUID = uuid4()
    order_id: UUID
    user_id: UUID
    items_total: int
    total_amount: Price
    status: InvoiceStatus = InvoiceStatus.PENDING

    def __str__(self):
        return  f"Invoice = ({self.__dict__})"
    #TODO: add other features
    #discount_amount
    #tax
    #shipping_cost