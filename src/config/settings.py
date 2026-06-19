from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    homeassistant_url: str = "https://homeassistant.aaronbotton.dev"
    homeassistant_token: str

    database_url: str = (
        "postgresql+psycopg://jarvis:jarvis@localhost:5432/jarvis"
    )


settings = Settings()