from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    finnhub_api_key: str = os.getenv("FINNHUB_API_KEY", "")
    finnhub_base_url: str = "https://finnhub.io/api/v1"
    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    alpha_vantage_base_url: str = "https://www.alphavantage.co/query"
    twelve_data_api_key: str = os.getenv("TWELVE_DATA_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = "gemini-1.5-flash"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    redis_url: Optional[str] = None
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    marketaux_api_key: str = os.getenv("MARKETAUX_API_KEY", "")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()
