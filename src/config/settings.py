from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str
    openai_model: str = "gpt-5.4"
    openai_embedding_model: str = "text-embedding-3-small"

    homeassistant_url: str = "https://homeassistant.aaronbotton.dev"
    homeassistant_token: str

    finances_url: str = "https://finances.aaronbotton.dev"
    diet_url: str = "https://diet.aaronbotton.dev"

    resend_api_key: str
    resend_from_email: str
    resend_to_email: str

    database_url: str = (
        "postgresql+psycopg://jarvis:jarvis@localhost:5432/jarvis"
    )

    @property
    def psycopg_url(self) -> str:
        return self.database_url.replace("postgresql+psycopg://", "postgresql://")


settings = Settings()