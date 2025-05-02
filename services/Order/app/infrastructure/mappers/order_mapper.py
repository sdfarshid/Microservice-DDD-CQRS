from __future__ import annotations

from uuid import UUID

from app.domain.order.entities.invoice import Invoice
from app.domain.order.aggregates.order import Order
from app.domain.order.entities.order_item import OrderItem
from app.domain.order.enums.invoice_status import InvoiceStatus
from app.domain.order.value_objects.price import Price
from app.infrastructure.database.models.invoice import InvoiceDBModel
from app.infrastructure.database.models.order import OrderDBModel
from app.infrastructure.database.models.order_item import OrderItemDBModel


class OrderMapper:

    @staticmethod
    def to_order_orm(domain_model: Order) -> OrderDBModel:
        return OrderDBModel(
            id=domain_model.id,
            user_id=domain_model.user_id,
            invoice_id=domain_model.invoice_id,
            status=domain_model.status.value,
            created_at=domain_model.created_at
        )

    @staticmethod
    def to_order_item_orm(item: OrderItem, order_id: UUID) -> OrderItemDBModel:
        return OrderItemDBModel(
            id=item.id,
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=item.price_at_order,
            status=item.status.value
        )

    @staticmethod
    def to_invoice_domain(invoice_db: InvoiceDBModel) -> Invoice:
        return Invoice(
            id=invoice_db.id,
            order_id=invoice_db.order_id,
            user_id=invoice_db.user_id,
            items_total=invoice_db.items_total,
           # discount_amount=invoice_db.discount_amount,   #  tax=invoice_db.tax,
          #  shipping_cost=invoice_db.shipping_cost,
            total_amount=Price(value=invoice_db.total_amount),
            status=InvoiceStatus(invoice_db.status)
        )

    @staticmethod
    def to_invoice_orm(invoice: Invoice) -> InvoiceDBModel:
        return InvoiceDBModel(
            id=invoice.id,
            order_id=invoice.order_id,
            user_id=invoice.user_id,
            items_total=invoice.items_total,
            total_amount=invoice.total_amount.value,
            status=invoice.status.value,
        )

    @staticmethod
    def make_invoice_domain(order: Order) -> Invoice:
        return Invoice(
            id=order.invoice_id,
            order_id=order.id,
            user_id=order.user_id,
            items_total=order.get_total_item(),
            total_amount=Price(value=order.get_total_amount()),
            status=InvoiceStatus.PENDING
        )


