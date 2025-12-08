"""
Configuration Settings for Levelith Backend

Manages environment variables and application settings using Pydantic Settings.
Supports multiple environments (development, staging, production).
"""

from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Neural Hive (AI & Vector DB)
    openai_api_key: str = "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"
    pinecone_api_key: str = "pcsk_4fnA2U_EMr42M8ufmrmFKsmWPWwnrQtjAdyed4CvgTAADbNKLRnn7nNdA3GaBxNshA2f2S"
    pinecone_index_name: str = "industry-classifier"
    pinecone_env: str = "us-east-1"  # or your specific region
    
    # Namespaces
    namespace_naics: str = "naics-codes"
    namespace_onet: str = "onet-codes"


    # Application
    app_name: str = "Levelith API"
    app_version: str = "2.0.0"
    debug: bool = False
    environment: str = "production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/levelith"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis Cache
    redis_url: str = "redis://localhost:6379"
    redis_cache_ttl: int = 300  # 5 minutes default

    # Security
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000,http://localhost:5173,https://levelith.online,https://www.levelith.online"
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # API Configuration
    api_v1_prefix: str = "/api/v1"
    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = {"development", "staging", "production", "test"}
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v.lower()

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return self.cors_origins

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def database_url_async(self) -> str:
        """Get async database URL for SQLAlchemy."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses LRU cache to ensure settings are loaded only once.
    """
    return Settings()


# Convenience export
settings = get_settings()
