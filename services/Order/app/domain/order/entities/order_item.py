from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.domain.order.enums.item_status import ItemStatus


class OrderItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    quantity: int
    price_at_order: float
    status: ItemStatus = ItemStatus.PENDING
