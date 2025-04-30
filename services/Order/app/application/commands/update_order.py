from uuid import UUID

from pydantic import BaseModel

from app.domain.order.enums.order_status import OrderStatus


class UpdateOrderCommand(BaseModel):
    order_id: UUID
    status: OrderStatus
