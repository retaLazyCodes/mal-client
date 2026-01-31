from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # MAL API
    MAL_CLIENT_ID: str = ""
    MAL_CLIENT_SECRET: str = ""
    MAL_CALLBACK_URL: str = ""
    
    # App
    SECRET_KEY: str = "dev-secret-key"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
