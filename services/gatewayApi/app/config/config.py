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
    CATALOG_SERVICE_URL: HttpUrl
    USER_SERVICE_URL: HttpUrl
    COMPANY_SERVICE_URL: HttpUrl
    ORDER_SERVICE_URL: HttpUrl



    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_GATEWAY}:5432/{self.POSTGRES_DB_GATEWAY}"

    @property
    def BASE_PATH(self):
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def get_service_url(self, service_name: str) -> str:
        self.set_services_routes()
        service_urls = {
            "company": self.COMPANY_BASE_URL,
            "product": self.PRODUCT_BASE_URL,
            "order": self.ORDER_BASE_URL,
            "user": self.USER_BASE_URL,
            "auth": self.AUTH_BASE_URL,
            "catalog": self.CATALOG_BASE_URL,
            "product_catalog": self.PRODUCT_CATALOG_BASE_URL,
            "gateway": self.API_GATEWAY_URL,
        }
        return service_urls.get(service_name, "Unknown service")

    def set_services_routes(self):
        self.COMPANY_BASE_URL = f"{self.COMPANY_SERVICE_URL}api/v1/company"
        self.PRODUCT_BASE_URL = f"{self.PRODUCT_SERVICE_URL}api/v1/product"
        self.ORDER_BASE_URL = f"{self.ORDER_SERVICE_URL}api/v1/order"
        self.USER_BASE_URL = f"{self.USER_SERVICE_URL}api/v1/user"
        self.AUTH_BASE_URL = f"{self.USER_SERVICE_URL}api/v1/auth"
        self.CATALOG_BASE_URL = f"{self.CATALOG_SERVICE_URL}api/v1/catalogs"
        self.PRODUCT_CATALOG_BASE_URL = f"{self.CATALOG_SERVICE_URL}api/v1/productCatalog"
        self.API_GATEWAY_URL = f"{self.API_GATEWAY_URL}api/v1/gateway"


settings = Settings()
