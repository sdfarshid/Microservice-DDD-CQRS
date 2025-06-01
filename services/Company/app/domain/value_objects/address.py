from pydantic import BaseModel, field_validator


class Address(BaseModel):
    value: str

    @classmethod
    @field_validator('value')
    def validate_address(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError("Address must be at least 10 characters")
        return v