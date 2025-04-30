from app.domain.order.events.order_cancelled import OrderCancelled
from app.application.services import OrderService


class OrderEventHandler:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def handle_order_cancelled(self, event: OrderCancelled):
        self.order_service.cancel_order(event.order_id)