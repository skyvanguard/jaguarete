"""Application configuration."""

from dataclasses import dataclass, field
import os


@dataclass
class Settings:
    """Jaguarete application settings."""

    app_name: str = "Jaguarete"
    app_version: str = "0.0.1"
    debug: bool = False

    # JWT
    secret_key: str = field(
        default_factory=lambda: os.getenv("JAGUARETE_SECRET_KEY", "change-me-in-production")
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    allowed_origins: list[str] = field(
        default_factory=lambda: os.getenv("JAGUARETE_CORS_ORIGINS", "http://localhost:3000").split(",")
    )

    # LLM
    default_llm_provider: str = field(
        default_factory=lambda: os.getenv("JAGUARETE_LLM_PROVIDER", "openai")
    )
    openai_api_key: str = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    anthropic_api_key: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "")
    )
    ollama_base_url: str = field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )


settings = Settings()
