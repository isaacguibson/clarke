from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://clarke:clarke123@localhost:5432/clarke_db"
    database_password: str = ""
    secret_key: str = "your-secret-key-here"
    debug: bool = True
    api_title: str = "Clarke Energia API"
    api_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
