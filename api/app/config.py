import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""
    
    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/clans_db"
    
    # Cloud SQL settings (for production)
    cloud_sql_connection_name: str = ""  # project:region:instance
    db_user: str = "postgres"
    db_password: str = ""
    db_name: str = "clans_db"
    
    # GCP settings
    gcp_project_id: str = ""
    gcp_region: str = "europe-west1"
    
    # App settings
    app_env: str = "development"  # development, production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Returns cached settings instance."""
    return Settings()
