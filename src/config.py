import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@db:5432/users")

    class Config:
        env_file = ".env"

settings = Settings()
