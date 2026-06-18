from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    homeassistant_url: str = "https://homeassistant.aaronbotton.dev"
    homeassistant_token: str

    database_url: str = (
        "postgresql+psycopg://jarvis:jarvis@localhost:5432/jarvis"
    )

    class Config:
        env_file = ".env"


settings = Settings()