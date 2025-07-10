from fastapi import Depends

from app.application.handlers import OrderHandler
from app.application.services.order_service import OrderService
from app.config.dependencies.handlers import get_order_handler
from app.application.services.invoice_service import InvoiceService
from app.application.services.payment_service import PaymentService
from app.application.services.product_service import ProductService
from app.application.handlers.invoice_handler import InvoiceHandler
from app.config.dependencies.handlers import get_invoice_handler
from app.utilities.gateway_client import GatewayClient
from app.infrastructure.events.kafka_producer import get_kafka_producer


def get_product_service():
    return ProductService(gateway_client=GatewayClient())


def get_payment_service():
    return PaymentService(gateway_client=GatewayClient(), kafka_producer=get_kafka_producer())


def get_invoice_service(handler: InvoiceHandler = Depends(get_invoice_handler)):
    return InvoiceService(invoice_handler=handler)


def get_order_service(
        order_handler: OrderHandler = Depends(get_order_handler),
        product_service: ProductService = Depends(get_product_service),
        payment_service: PaymentService = Depends(get_payment_service),
        invoice_service: InvoiceService = Depends(get_invoice_service),
):
    return OrderService(order_handler=order_handler,
                        product_service=product_service,
                        payment_service=payment_service,
                        invoice_service=invoice_service
                        )



