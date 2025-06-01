from pydantic_settings import BaseSettings, SettingsConfigDict


class ShareSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="shared/.envGateWay",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )
    GATEWAY_API_KEY: str


share_setting = ShareSetting()

