from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    postgres_url: str = (
        "postgresql://jarvis:jarvis@localhost:5432/jarvis"
    )

    class Config:
        env_file = ".env"


settings = Settings()