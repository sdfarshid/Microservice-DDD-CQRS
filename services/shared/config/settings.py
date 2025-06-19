import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class ShareSetting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="shared/.envGateWay",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )
    GATEWAY_API_KEY: str
    PUBLIC_KEY_PATH: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

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


share_setting = ShareSetting()

