from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    INFURA_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

print(f"Loaded settings: {settings.dict()}")
