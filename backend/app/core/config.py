"""
Application configuration using Pydantic Settings.
"""
from typing import List

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "AI Book Platform"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/aibook"

    @model_validator(mode='after')
    def validate_configs(self):
        """Validate and fix configurations."""
        # Ensure the database URL uses the asyncpg driver
        if self.DATABASE_URL.startswith("postgresql://") and not self.DATABASE_URL.startswith("postgresql+asyncpg://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Validate OpenRouter model
        valid_models = [
            "anthropic/claude-3.5-sonnet", "anthropic/claude-3-haiku",
            "openai/gpt-4o", "openai/gpt-4o-mini", "openai/gpt-4-turbo",
            "google/gemini-pro", "google/gemini-flash",
            "meta-llama/llama-3.1-405b-instruct", "meta-llama/llama-3.1-70b-instruct"
        ]

        if self.OPENROUTER_MODEL not in valid_models:
            print(f"Warning: Invalid OpenRouter model '{self.OPENROUTER_MODEL}', defaulting to 'anthropic/claude-3.5-sonnet'")
            self.OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"

        return self

    # Vector Database (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "book_content"

    # OpenRouter (for LLM chat completions)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"

    # Cohere (for embeddings)
    COHERE_API_KEY: str = ""
    COHERE_EMBEDDING_MODEL: str = "embed-english-v3.0"

    # Legacy OpenAI settings (fallback)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # LLM Provider choice: "openrouter" or "openai"
    LLM_PROVIDER: str = "openrouter"

    # Authentication
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS - stored as comma-separated string
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"

    # Redis (for caching)
    REDIS_URL: str = "redis://localhost:6379"

    @computed_field
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
