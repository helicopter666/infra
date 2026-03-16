from pydantic import Field, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Database ──────────────────────────────────────────────────
    DATABASE_URL: PostgresDsn

    # ── Redis ─────────────────────────────────────────────────────
    REDIS_URL: RedisDsn

    # ── Redpanda / Kafka ──────────────────────────────────────────
    REDPANDA_BOOTSTRAP_SERVERS: str

    # ── JWT ───────────────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── LLM ───────────────────────────────────────────────────────
    OPENROUTER_API_KEY: str
    LLM_MODEL: str = "google/gemini-2.0-flash-thinking-exp"
    LLM_TIMEOUT_SECONDS: int = 60
    LLM_MAX_RETRIES: int = 3

    # ── App ───────────────────────────────────────────────────────
    APP_ENV: str = Field(default="development", pattern="^(development|production|test)$")
    DEBUG: bool = False


settings = Settings()
