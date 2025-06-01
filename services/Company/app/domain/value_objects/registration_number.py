import re
from pydantic import BaseModel, field_validator


class RegistrationNumber(BaseModel):
    value: str

    def __init__(self, value: str):
        super().__init__(value=value)

    @field_validator('value')
    @classmethod
    def validate_registration_number(cls, value: str) -> str:
        value = value.strip()
        if not value or len(value) < 3:
            raise ValueError("Registration number must be at least 5 characters")
        return value

    def __str__(self) -> str:
        return self.value
