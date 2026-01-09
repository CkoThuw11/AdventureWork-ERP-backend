"""Application Configuration.

This module handles application configuration using Pydantic Settings.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="tinybigcorp", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="postgres", description="Database password")
    pool_size: int = Field(default=20, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Maximum pool overflow")

    @property
    def url(self) -> str:
        """Get the database connection URL.

        Returns:
            PostgreSQL connection URL.
        """
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class AppSettings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(env_prefix="APP_")

    name: str = Field(default="TinyBigCorp Backend", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    env: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")


class APISettings(BaseSettings):
    """API configuration settings."""

    model_config = SettingsConfigDict(env_prefix="API_")

    v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    cors_origins: str = Field(
        default="http://localhost:4200", description="CORS allowed origins (comma-separated)"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list.

        Returns:
            List of allowed CORS origins.
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]


class LogSettings(BaseSettings):
    """Logging configuration settings."""

    model_config = SettingsConfigDict(env_prefix="LOG_")

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(default="json", description="Log format (json or console)")


class Settings(BaseSettings):
    """Main application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    api: APISettings = Field(default_factory=APISettings)
    log: LogSettings = Field(default_factory=LogSettings)


# Global settings instance
settings = Settings()
