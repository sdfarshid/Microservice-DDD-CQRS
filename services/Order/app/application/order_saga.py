from uuid import uuid4

from app.application.services.invoice_service import InvoiceService
from app.application.services.product_service import ProductService
from app.domain.order.aggregates.order import Order
from shared.domain.order.commands.create_order import CreateOrderCommand
from app.utilities.log import DebugError, DebugWarning


class OrderCreationSaga:
    def __init__(self, order_service, product_service: ProductService,
                 invoice_service: InvoiceService,
                 ):
        self.order_service = order_service
        self.product_service = product_service
        self.invoice_service = invoice_service

    async def execute(self, command: CreateOrderCommand) -> dict:
        order = None
        invoice = None
        try:
            # Step 1: Create order Items with product validation
            DebugWarning(f"Creating order items for user: {command.user_id}")
            items = await self.product_service.create_order_items(command.items)

            # Step 2: Create order and store
            order = Order.create(user_id=command.user_id, items=items, invoice_id=uuid4())
            DebugWarning(f"Created order: {order.id}")

            # Create order through service
            created_order = await self.order_service.create_order_with_items(order, items)
            DebugWarning(f"Order and items stored: {created_order.id}")

            # Step 3: Create Invoice
            invoice = await self.invoice_service.create_invoice(created_order)
            DebugWarning(f"Created invoice: {invoice.id}")

            # Step 4: Reserve Products
            DebugWarning(f"Reserving products for order: {created_order.id}")
            await self.product_service.reserve_products(created_order.id, items)

            # Step 5: Update items to reserved status through service
            await self.order_service.mark_items_as_reserved(created_order.id, items)
            DebugWarning(f"Items marked as reserved for order: {created_order.id}")

            # Step 6: Confirm order through service
            await self.order_service.confirm_order(created_order.id)
            DebugWarning(f"Order confirmed: {created_order.id}")

            return {
                "order_id": created_order.id,
                "invoice_id": invoice.id,
                "total_amount": created_order.get_total_amount(),
                "status": "payment_pending"
            }
        except Exception as e:
            DebugError(f"Error in order saga: {str(e)}")
            if order:
                try:
                    await self._compensate_order(order)
                except Exception as comp_error:
                    DebugError(f"Compensation failed: {str(comp_error)}")
            raise e

    async def _compensate_order(self, order: Order):
        """Compensate/rollback order in case of failure"""
        try:
            # Cancel order through service
            await self.order_service.cancel_order(order.id)

            # Cancel invoice through service
            await self.invoice_service.cancel_invoice(order.invoice_id)

            # Release reserved products
            await self.product_service.release_products(order.id, order.items)

            DebugWarning(f"Order {order.id} compensated successfully")
        except Exception as e:
            DebugError(f"Failed to compensate order {order.id}: {str(e)}")
            raise e
