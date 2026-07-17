from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    AI_PROVIDER: str = "ollama"

    OLLAMA_URL: str = (
        "http://127.0.0.1:11434/api/generate"
    )

    OLLAMA_MODEL: str = "qwen2.5:7b"


    class Config:
        env_file = ".env"


settings = Settings()
