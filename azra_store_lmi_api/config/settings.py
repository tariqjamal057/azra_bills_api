"""Application settings module.

This module loads application settings from environment variables and a .env file.
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class defines the configuration settings for the application,
    including database connections, authentication secrets, email settings,
    and various API endpoints.

    Attributes:
        Attributes are dynamically set based on environment variables.
        See the class body for a list of supported configuration options.
    """

    DATABASE_URL: str
    ENVIRONMENT: Literal["development", "testing", "production"]
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_USE_SSL: bool
    MAIL_USE_TLS: bool
    ADMIN_APP_BASE_URL: str
    TENANT_APP_BASE_URL: str
    CELERY_BROKER_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
