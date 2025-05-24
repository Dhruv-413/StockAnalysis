import os
from dotenv import load_dotenv

load_dotenv()

# Google ADK & Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-1.5-flash-latest") # Default if not set

# Stock Data APIs
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY") # Assuming MarketAux or NewsAPI might be used

# Redis Cache (optional)
REDIS_URL = os.getenv("REDIS_URL")

# Rate Limiting (example, not directly used by ADK agents typically)
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API Base URLs (example)
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Simple validation for critical keys
REQUIRED_KEYS = {
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    # Add other critical API keys here if needed for core functionality
    # e.g., "ALPHA_VANTAGE_API_KEY": ALPHA_VANTAGE_API_KEY,
}

missing_keys = [key for key, value in REQUIRED_KEYS.items() if not value]
if missing_keys:
    raise ValueError(f"Missing critical environment variables: {', '.join(missing_keys)}")

if not ALPHA_VANTAGE_API_KEY:
    print("Warning: ALPHA_VANTAGE_API_KEY is not set. Functionality requiring it will be limited.")

if __name__ == "__main__":
    # For testing the config loading
    print(f"Google API Key Loaded: {bool(GOOGLE_API_KEY)}")
    print(f"Gemini Model: {GEMINI_MODEL}")
    print(f"Finnhub API Key Loaded: {bool(FINNHUB_API_KEY)}")
    print(f"Twelve Data API Key Loaded: {bool(TWELVE_DATA_API_KEY)}")
    print(f"Alpha Vantage API Key Loaded: {bool(ALPHA_VANTAGE_API_KEY)}")
    print(f"Redis URL: {REDIS_URL}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Log Level: {LOG_LEVEL}")

