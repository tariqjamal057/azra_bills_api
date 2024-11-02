"""Application settings module.

This module loads application settings from environment variables and a .env file.
"""

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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
