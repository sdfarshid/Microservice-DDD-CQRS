from fastapi import Depends

from app.application.commands.create_order import CreateOrderCommand
from app.application.handlers.order_handler import OrderHandler
from app.domain.order.entities.invoice import Invoice


class OrderService:
    def __init__(
            self,
            order_handler: OrderHandler = Depends(OrderHandler),
    ):
        self.handler = order_handler

    async def create_order(self, command: CreateOrderCommand) -> Invoice:
        return await self.handler.create(command)

