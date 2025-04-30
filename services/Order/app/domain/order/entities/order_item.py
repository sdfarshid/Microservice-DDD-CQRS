from uuid import UUID, uuid4
from pydantic import BaseModel
from app.domain.order.enums.item_status import ItemStatus


class OrderItem(BaseModel):
    id: UUID = uuid4()
    product_id: UUID
    quantity: int
    price_at_order: float
    status: ItemStatus = ItemStatus.PENDING
