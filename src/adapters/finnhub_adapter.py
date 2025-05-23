from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base_adapter import BaseAdapter
from src.config import settings
from src.utils.cache import cached

class FinnhubAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            api_key=settings.finnhub_api_key,
            base_url="https://finnhub.io/api/v1"
        )
    
    def _get_auth_params(self) -> Dict[str, str]:
        return {"token": self.api_key}
    
    @cached(ttl=3600)  # Cache for 1 hour
    async def search_ticker(self, company_name: str) -> Optional[str]:
        """Search for ticker symbol by company name"""
        try:
            data = await self._make_request("search", {"q": company_name})
            results = data.get("result", [])
            
            if results:
                # Return the first result's symbol
                return results[0].get("symbol")
            return None
        except Exception as e:
            self.logger.error(f"Error searching ticker for {company_name}: {e}")
            return None
    
    @cached(ttl=300)  # Cache for 5 minutes
    async def get_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get current price quote for ticker"""
        try:
            data = await self._make_request("quote", {"symbol": ticker})
            return {
                "current_price": data.get("c"),
                "previous_close": data.get("pc"),
                "change": data.get("d"),
                "change_percent": data.get("dp"),
                "high": data.get("h"),
                "low": data.get("l"),
                "volume": data.get("v")
            }
        except Exception as e:
            self.logger.error(f"Error getting quote for {ticker}: {e}")
            return None
    
    @cached(ttl=1800)  # Cache for 30 minutes
    async def get_company_news(self, ticker: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get company news for the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                "symbol": ticker,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            }
            
            data = await self._make_request("company-news", params)
            
            news_items = []
            for article in data[:10]:  # Limit to 10 most recent
                news_items.append({
                    "title": article.get("headline", ""),
                    "summary": article.get("summary", ""),
                    "source": article.get("source", ""),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)),
                    "url": article.get("url", ""),
                    "sentiment": None  # Will be analyzed by Gemini
                })
            
            return news_items
        except Exception as e:
            self.logger.error(f"Error getting news for {ticker}: {e}")
            return []
    
    @cached(ttl=3600)  # Cache for 1 hour
    async def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get company profile information"""
        try:
            data = await self._make_request("stock/profile2", {"symbol": ticker})
            return {
                "name": data.get("name"),
                "ticker": data.get("ticker"),
                "exchange": data.get("exchange"),
                "industry": data.get("finnhubIndustry"),
                "market_cap": data.get("marketCapitalization"),
                "website": data.get("weburl"),
                "description": data.get("description")
            }
        except Exception as e:
            self.logger.error(f"Error getting profile for {ticker}: {e}")
            return None

    @cached(ttl=86400) # Cache for 1 day
    async def get_financials_as_reported(self, ticker: str, freq: str = "annual") -> Optional[Dict[str, Any]]:
        """Get financials as reported (income, balance sheet, cash flow). Freq: annual, quarterly"""
        try:
            params = {"symbol": ticker, "freq": freq}
            data = await self._make_request("stock/financials-reported", params)
            return data
        except Exception as e:
            self.logger.error(f"Error getting financials for {ticker}: {e}")
            return None

    @cached(ttl=3600) # Cache for 1 hour
    async def get_stock_candles(self, ticker: str, resolution: str, from_timestamp: int, to_timestamp: int) -> Optional[List[Dict[str, Any]]]:
        """Get stock candles. Resolution: 1, 5, 15, 30, 60, D, W, M"""
        try:
            params = {
                "symbol": ticker,
                "resolution": resolution,
                "from": from_timestamp,
                "to": to_timestamp
            }
            data = await self._make_request("stock/candle", params)
            if data and data.get("s") == "ok":
                candles = []
                for i in range(len(data.get("t", []))):
                    candles.append({
                        "open": data["o"][i],
                        "high": data["h"][i],
                        "low": data["l"][i],
                        "close": data["c"][i],
                        "volume": data["v"][i],
                        "timestamp": data["t"][i]
                    })
                return candles
            elif data and data.get("s") == "no_data":
                self.logger.info(f"No candle data for {ticker} with params: {params}")
                return []
            return None
        except Exception as e:
            self.logger.error(f"Error getting stock candles for {ticker}: {e}")
            return None

    @cached(ttl=86400) # Cache for 1 day
    async def get_earnings_calendar(self, ticker: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get earnings calendar. Dates YYYY-MM-DD"""
        try:
            params = {}
            if ticker: params["symbol"] = ticker
            if from_date: params["from"] = from_date
            if to_date: params["to"] = to_date
            # Use a default date range if none provided to avoid fetching too much data
            if not from_date and not to_date:
                today = datetime.now()
                params["from"] = (today - timedelta(days=7)).strftime("%Y-%m-%d")
                params["to"] = (today + timedelta(days=30)).strftime("%Y-%m-%d")

            data = await self._make_request("calendar/earnings", params)
            return data.get("earningsCalendar", [])
        except Exception as e:
            self.logger.error(f"Error getting earnings calendar: {e}")
            return None

    @cached(ttl=86400) # Cache for 1 day
    async def get_ipo_calendar(self, from_date: str, to_date: str) -> Optional[List[Dict[str, Any]]]:
        """Get IPO calendar. Dates YYYY-MM-DD"""
        try:
            params = {"from": from_date, "to": to_date}
            data = await self._make_request("calendar/ipo", params)
            return data.get("ipoCalendar", [])
        except Exception as e:
            self.logger.error(f"Error getting IPO calendar: {e}")
            return None

    @cached(ttl=86400) # Cache for 1 day
    async def get_dividend_calendar(self, ticker: str, from_date: str, to_date: str) -> Optional[List[Dict[str, Any]]]:
        """Get dividend data. Dates YYYY-MM-DD"""
        try:
            params = {"symbol": ticker, "from": from_date, "to": to_date}
            data = await self._make_request("stock/dividend2", params) # dividend2 is recommended
            return data
        except Exception as e:
            self.logger.error(f"Error getting dividend calendar for {ticker}: {e}")
            return None

    @cached(ttl=86400) # Cache for 1 day
    async def get_stock_splits(self, ticker: str, from_date: str, to_date: str) -> Optional[List[Dict[str, Any]]]:
        """Get stock splits. Dates YYYY-MM-DD"""
        try:
            params = {"symbol": ticker, "from": from_date, "to": to_date}
            data = await self._make_request("stock/split", params)
            return data
        except Exception as e:
            self.logger.error(f"Error getting stock splits for {ticker}: {e}")
            return None
            
    @cached(ttl=3600) # Cache for 1 hour
    async def get_insider_transactions(self, ticker: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """Get insider transactions. Dates YYYY-MM-DD"""
        try:
            params = {"symbol": ticker}
            if from_date: params["from"] = from_date
            if to_date: params["to"] = to_date
            data = await self._make_request("stock/insider-transactions", params)
            return data.get("data", [])
        except Exception as e:
            self.logger.error(f"Error getting insider transactions for {ticker}: {e}")
            return None

    @cached(ttl=1800) # Cache for 30 minutes
    async def get_general_market_news(self, category: str = "general", min_id: int = 0) -> List[Dict[str, Any]]:
        """Get general market news. Category can be general, forex, crypto, merger."""
        try:
            params = {"category": category}
            if min_id > 0: # For pagination, though not fully implemented here
                params["minId"] = min_id
            
            data = await self._make_request("news", params) # General news endpoint
            
            news_items = []
            for article in data[:20]: # Limit to 20 most recent
                news_items.append({
                    "title": article.get("headline", ""),
                    "summary": article.get("summary", ""),
                    "source": article.get("source", ""),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)),
                    "url": article.get("url", ""),
                    "category": article.get("category")
                })
            return news_items
        except Exception as e:
            self.logger.error(f"Error getting general market news for category {category}: {e}")
            return []
