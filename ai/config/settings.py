from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    AI_PROVIDER: str = "ollama"

    REDIS_URL: str = "redis://localhost:6379"

    OLLAMA_URL: str = (
        "http://ollama:11434/api/generate"
    )

    OLLAMA_MODEL: str = (
        "qwen2.5:7b"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
