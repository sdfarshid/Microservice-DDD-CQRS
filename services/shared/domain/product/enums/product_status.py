from enum import Enum


class ProductStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]
