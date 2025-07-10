
from app.domain.order.entities.invoice import Invoice
from app.domain.order.interface.IOrder_repository import IOrderRepository


class InvoiceHandler:
    def __init__(self, repository: IOrderRepository):
        self.repository = repository

    async def create(self, invoice: Invoice):
        return await self.repository.add_invoice(invoice)
