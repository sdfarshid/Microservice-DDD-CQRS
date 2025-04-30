from uuid import UUID

from pydantic import BaseModel


class OrderCancelled(BaseModel):
    order_id: UUID
    user_id: UUID