from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    google_api_key: str
    gemini_model: str = "gemini-pro"
    
    finnhub_api_key: str
    twelve_data_api_key: Optional[str] = None # New API Key
    
    redis_url: Optional[str] = None
    
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
