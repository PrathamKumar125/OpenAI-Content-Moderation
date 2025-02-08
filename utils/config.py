from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Content Moderation Service"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()