from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    OUR_TEAM_ID: int

    FIRST_API_USERNAME: str
    FIRST_API_TOKEN: str
    FIRST_API_SEASON: int = 2024

    FIRST_API_BASE_URL: str = "https://ftc-api.firstinspires.org"


settings = Settings()
