from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.order.enums.order_status import OrderStatus


class UpdateOrderItemCommand(BaseModel):
    order_item_id: UUID
    order_id: UUID
    status: OrderStatus
    updated_data: datetime = datetime.now()
