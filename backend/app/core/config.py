from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./scouting.db"

    FIRST_API_USERNAME: str
    FIRST_API_TOKEN: str
    FIRST_API_SEASON: int = 2024

    OUR_TEAM_ID: int = 0

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
