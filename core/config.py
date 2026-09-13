from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()