from pydantic import BaseModel, field_validator


class Price(BaseModel):
    value: float

    @classmethod
    @field_validator('value')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v