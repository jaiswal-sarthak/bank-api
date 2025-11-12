"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    app_name: str = "Indian Bank Branches API"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./bank_branches.db"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
