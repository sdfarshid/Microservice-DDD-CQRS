from enum import Enum


class ItemStatus(Enum):
    PENDING = "PENDING"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]


