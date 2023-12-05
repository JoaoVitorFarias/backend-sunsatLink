import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str = os.getenv('DATABASE_URL', "postgres://postgres:postgres@db:5432/users").replace("://", "ql://", 1)

    class Config:
        env_file = ".env"

settings = Settings()
