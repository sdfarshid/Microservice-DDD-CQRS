from pydantic import BaseModel, field_validator


class SKU(BaseModel):
    value: str

    @classmethod
    @field_validator('value')
    def validate_price(cls, v):
        if not v or len(v) > 50:
            raise ValueError("SKU must be a non-empty string with a maximum length of 50 characters.")
        return v

    def __str__(self) -> str:
        return self.value
