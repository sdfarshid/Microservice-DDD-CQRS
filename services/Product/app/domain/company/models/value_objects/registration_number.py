from pydantic import BaseModel, field_validator


class RegistrationNumber(BaseModel):
    value: str

    @classmethod
    @field_validator('value')
    def validate_number(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError("Registration number must be at least 5 characters")
        return v
