import logging
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base_adapter import BaseAdapter
from src.config import settings
from ..utils.cache import cached

class MarketauxAdapter(BaseAdapter):
    """Adapter for fetching news data from Marketaux API."""
    
    def __init__(self):
        api_key = settings.marketaux_api_key
        if not api_key or api_key == "YOUR_MARKETAUX_API_KEY_HERE":
            self.logger.warning("Marketaux API key is not properly configured. Adapter functionality will be limited.")
        
        super().__init__(
            api_key=api_key or "DUMMY_KEY_IF_NONE",
            base_url="https://api.marketaux.com/v1"
        )
        
        if not api_key or api_key == "YOUR_MARKETAUX_API_KEY_HERE":
            self.api_key = None
            
    def _get_auth_params(self) -> Dict[str, str]:
        if not self.api_key:
            return {}
        return {"api_token": self.api_key}
    
    @cached(ttl=1800)  # Cache for 30 minutes
    async def get_company_news(self, ticker: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get news articles for a specific company/ticker."""
        if not self.api_key:
            self.logger.error(f"Marketaux API key not configured. Cannot fetch news for {ticker}.")
            return []
            
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                "symbols": ticker,
                "limit": 10,
                "published_after": start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "language": "en"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.base_url}/news/all", params={**params, **self._get_auth_params()})
                response.raise_for_status()
                
            data = response.json()
            
            if "data" not in data:
                self.logger.warning(f"No news data from Marketaux for {ticker}")
                return []
                
            news_items = []
            for article in data["data"]:
                # Convert ISO timestamp to datetime
                try:
                    published_at = datetime.strptime(article.get("published_at", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
                except (ValueError, TypeError):
                    published_at = datetime.now()
                
                news_items.append({
                    "title": article.get("title", ""),
                    "summary": article.get("description", ""),
                    "source": article.get("source", ""),
                    "published_at": published_at,
                    "url": article.get("url", ""),
                    "related": ticker,
                    "sentiment": None  # Will be analyzed by Gemini
                })
                
            return news_items
            
        except Exception as e:
            self.logger.error(f"Error getting Marketaux news for {ticker}: {e}")
            return []