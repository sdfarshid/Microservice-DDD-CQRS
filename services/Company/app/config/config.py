from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_COMPANY: str
    POSTGRES_HOST_COMPANY: str
    POSTGRES_PORT_COMPANY: str
    APP_PORT_COMPANY: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_COMPANY}:5432/{self.POSTGRES_DB_COMPANY}"



settings = Settings()

print(settings.DATABASE_URL)

