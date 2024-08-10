# /app/core/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    INFURA_API_KEY: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    REDIS_URL: str = "redis://localhost:6388/0"

    class Config:
        env_file = ".env"


settings = Settings()
