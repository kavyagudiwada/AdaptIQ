"""Application settings loaded from environment variables / .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Database -------------------------------------------------------
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/learnai"

    # --- AI provider ----------------------------------------------------
    ai_provider: str = "gemini"
    # Generic key (OpenAI, or fallback for any provider).
    ai_api_key: str = ""
    ai_model: str = "gemini-2.5-flash"
    # Gemini-standard aliases. When AI_PROVIDER=gemini these are preferred, so
    # a stock `GEMINI_API_KEY`/`GEMINI_MODEL` in .env drives the app directly.
    gemini_api_key: str = ""
    gemini_model: str = ""

    # --- App ------------------------------------------------------------
    frontend_url: str = "http://localhost:5173"
    app_name: str = "AdaptIQ API"
    version: str = "1.0.0"
    debug: bool = False

    # --- Auth ------------------------------------------------------------
    # Leave empty in development and an ephemeral key is generated at runtime
    # (tokens then reset on restart). Always set it in production.
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60 * 24 * 7  # 7 days

    # --- Google sign-in (optional) ---------------------------------------
    # Leave both blank to hide Google sign-in. The redirect URI to register with
    # Google is `{backend_url}/api/auth/google/callback`.
    google_client_id: str = ""
    google_client_secret: str = ""

    @property
    def google_enabled(self) -> bool:
        return bool(self.google_client_id.strip() and self.google_client_secret.strip())

    @property
    def resolved_api_key(self) -> str:
        if self.ai_provider.strip().lower() == "gemini":
            return (self.gemini_api_key or self.ai_api_key).strip()
        return self.ai_api_key.strip()

    @property
    def resolved_model(self) -> str:
        if self.ai_provider.strip().lower() == "gemini":
            return (self.gemini_model or self.ai_model).strip()
        return self.ai_model.strip()

    @property
    def ai_mode(self) -> str:
        """'live' when a provider key is configured, otherwise the local bank."""
        return "live" if self.resolved_api_key else "offline"

    @property
    def ai_enabled(self) -> bool:
        return self.ai_mode == "live"

    def safe_dict(self) -> dict[str, str]:
        """Settings safe to log or return over HTTP (no secrets)."""
        return {
            "ai_provider": self.ai_provider,
            "ai_model": self.resolved_model,
            "ai_mode": self.ai_mode,
            "frontend_url": self.frontend_url,
            "app_name": self.app_name,
            "version": self.version,
            "debug": self.debug,
            "google_enabled": self.google_enabled,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
