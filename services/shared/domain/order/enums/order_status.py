from enum import Enum


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    SHIPPED = "SHIPPED"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]
