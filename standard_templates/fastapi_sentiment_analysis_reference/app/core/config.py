from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    model_name: str = Field(
        default="tabularisai/multilingual-sentiment-analysis",
        alias="MODEL_NAME",
    )
    model_task: str = Field(default="text-classification", alias="MODEL_TASK")
    max_input_chars: int = Field(default=5000, alias="MAX_INPUT_CHARS", ge=1)
    model_load_on_startup: bool = Field(
        default=True,
        alias="MODEL_LOAD_ON_STARTUP",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

