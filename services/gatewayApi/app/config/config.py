import os

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
    POSTGRES_DB_GATEWAY: str
    POSTGRES_HOST_GATEWAY: str
    POSTGRES_PORT_GATEWAY: str
    APP_PORT_GATEWAY: str

    API_GATEWAY_URL: HttpUrl
    KAFKA_BOOTSTRAP_SERVERS: HttpUrl
    PRODUCT_SERVICE_URL: HttpUrl
    USER_SERVICE_URL: HttpUrl
    COMPANY_SERVICE_URL: HttpUrl
    ORDER_SERVICE_URL: HttpUrl

    PUBLIC_KEY_PATH: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_GATEWAY}:5432/{self.POSTGRES_DB_GATEWAY}"

    @property
    def BASE_PATH(self):
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @property
    def PUBLIC_KEY(self):
        public_key_path = self.get_public_key_path()
        with open(public_key_path, "r") as f:
            PUBLIC_KEY = f.read()
        return PUBLIC_KEY

    def get_public_key_path(self) -> str:
        public_key_full_path = os.path.join(self.BASE_PATH, self.PUBLIC_KEY_PATH)
        if not os.path.exists(public_key_full_path):
            raise FileNotFoundError(f"Public key file not found at: {public_key_full_path}")
        return public_key_full_path

    def get_service_url(self, service_name: str) -> str:
        self.set_services_routes()
        service_urls = {
            "company": self.COMPANY_BASE_URL,
            "product": self.PRODUCT_BASE_URL,
            "order": self.ORDER_BASE_URL,
            "user": self.USER_BASE_URL,
            "gateway": self.API_GATEWAY_URL,
        }
        return service_urls.get(service_name, "Unknown service")

    def set_services_routes(self):
        self.COMPANY_BASE_URL = f"{self.COMPANY_SERVICE_URL}api/v1/company"
        self.PRODUCT_BASE_URL = f"{self.PRODUCT_SERVICE_URL}api/v1/product"
        self.ORDER_BASE_URL = f"{self.ORDER_SERVICE_URL}api/v1/order"
        self.USER_BASE_URL = f"{self.USER_SERVICE_URL}api/v1/user"
        self.API_GATEWAY_URL = f"{self.API_GATEWAY_URL}api/v1/gateway"


settings = Settings()
