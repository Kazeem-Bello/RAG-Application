from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


file_path = Path(__file__).parents[1]

class Settings (BaseSettings):
    
    OPENAI_API_KEY: str
    OLLAMA_BASE_MODEL: str
    QDRANT_BASE_URL: str
    
    
    
    model_config = SettingsConfigDict(
        env_file=f"{file_path}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    
settings = Settings()