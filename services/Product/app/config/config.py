from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, HttpUrl


class Settings(BaseSettings):


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_PRODUCT: str
    POSTGRES_HOST_PRODUCT: str
    POSTGRES_PORT_PRODUCT: str
    APP_PORT_PRODUCT: str
    GATEWAY_SERVICE_URL: HttpUrl

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_PRODUCT}:5432/{self.POSTGRES_DB_PRODUCT}"



settings = Settings()

print(settings.DATABASE_URL)

