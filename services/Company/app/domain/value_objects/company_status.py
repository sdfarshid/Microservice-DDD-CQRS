from enum import Enum
from pydantic import BaseModel, field_validator

from app.utilities.log import DebugWaring
from shared import CompanyStatusEnum


class CompanyStatus(BaseModel):
    value: str

    def __init__(self, value: str):
        super().__init__(value=value)

    @field_validator('value')
    @classmethod
    def validate_status(cls, value: str) -> str:
        try:
            status = CompanyStatusEnum(value.lower())
            return status.value
        except ValueError:
            valid_statuses = ", ".join([s.value for s in CompanyStatusEnum])
            raise ValueError(f"Invalid company status. Valid statuses are: {valid_statuses}")

    def __str__(self) -> str:
        return self.value
