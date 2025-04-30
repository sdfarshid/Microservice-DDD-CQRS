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
    POSTGRES_DB_ORDER: str
    POSTGRES_HOST_ORDER: str
    POSTGRES_PORT_ORDER: str
    APP_PORT_ORDER: str
    API_GATEWAY_URL: HttpUrl
    KAFKA_BOOTSTRAP_SERVERS: HttpUrl
    INVOICE_EXPIRED_TIME_MINUTES: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_ORDER}:5432/{self.POSTGRES_DB_ORDER}"

    @staticmethod
    def get_expired_time(self) -> int:
        return self.INVOICE_EXPIRED_TIME_MINUTES #10 Min


settings = Settings()
