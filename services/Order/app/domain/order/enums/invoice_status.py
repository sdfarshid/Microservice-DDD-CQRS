from enum import Enum


class InvoiceStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]

