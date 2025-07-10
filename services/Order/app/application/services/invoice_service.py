from typing import List
from uuid import UUID
from fastapi import Depends

from app.application.handlers.invoice_handler import InvoiceHandler
from app.domain.order.entities.invoice import Invoice
from app.domain.order.value_objects.price import Price
from shared.domain.order.enums.invoice_status import InvoiceStatus
from app.utilities.log import DebugWarning, DebugError


class InvoiceService:
    def __init__(self, invoice_handler: InvoiceHandler):
        self.handler = invoice_handler

    async def create_invoice(self, order) -> Invoice:
        DebugWarning(f"Creating invoice for order: {order.id}")

        invoice = Invoice(
            id=order.invoice_id,
            order_id=order.id,
            user_id=order.user_id,
            items_total=order.get_total_item(),
            total_amount=Price(value=order.get_total_amount()),
            status=InvoiceStatus.PENDING
        )
        created_invoice = await self.handler.create(invoice)
        DebugWarning(f"Invoice created: {created_invoice.id}")
        return created_invoice

    async def cancel_invoice(self, invoice_id: UUID) -> None:
        """Cancel an invoice by updating its status to failed"""
        DebugWarning(f"Cancelling invoice: {invoice_id}")
        await self.handler.repository.update_invoice_status(invoice_id, InvoiceStatus.FAILED)

    async def mark_invoice_as_paid(self, invoice_id: UUID) -> None:
        """Mark an invoice as paid"""
        DebugWarning(f"Marking invoice as paid: {invoice_id}")
        await self.handler.repository.update_invoice_status(invoice_id, InvoiceStatus.PAID)

    async def get_invoice_by_id(self, invoice_id: UUID) -> Invoice:
        """Get invoice by ID"""
        return await self.handler.repository.get_invoice_by_id(invoice_id)
