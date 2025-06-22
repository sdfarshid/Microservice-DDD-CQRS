from pydantic import BaseModel, field_validator


class CatalogName(BaseModel):
    value: str

    @classmethod
    @field_validator('value')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError("Catalog name must be at least 2 characters")
        return v

    def __str__(self) -> str:
        return self.value
