# In app/core/config.py (No changes needed, current state is fine)

from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Database URL: This will be overridden by the environment variable from Docker Compose
    DATABASE_URL: str = (
        "sqlite:///./address_book.db"  # Default for local non-docker run
    )

    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", extra="ignore"
    )


settings = Settings()
