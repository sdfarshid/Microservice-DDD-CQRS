from enum import Enum


class CompanyStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]

