from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    finnhub_api_key: str = os.getenv("FINNHUB_API_KEY", "")
    finnhub_base_url: str = "https://finnhub.io/api/v1"
    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    alpha_vantage_base_url: str = "https://www.alphavantage.co/query"
    twelve_data_api_key: str = os.getenv("TWELVE_DATA_API_KEY", "")  # Add this field
    
    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = "gemini-pro"
    
    # Application Configuration
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Cache Configuration
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    
    redis_url: Optional[str] = None
    
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8' # Ensure .env is read correctly
        extra = "ignore"  # Add this to ignore extra environment variables

settings = Settings()

# Optional: Add a check for Alpha Vantage key if it's critical for some flows
# if not settings.alpha_vantage_api_key:
#     print("Warning: ALPHA_VANTAGE_API_KEY is not set in .env. Price change features will be limited.")
