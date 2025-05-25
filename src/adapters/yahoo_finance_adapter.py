import logging
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from .base_adapter import BaseAdapter
from ..utils.cache import cached

class YahooFinanceAdapter(BaseAdapter):
    """Adapter for fetching stock data from Yahoo Finance API using yfinance package."""
    
    def __init__(self):
        super().__init__(api_key=None, base_url=None)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _get_auth_params(self) -> Dict[str, str]:
        return {}  # Yahoo Finance doesn't need authentication
    
    @cached(ttl=300)  # Cache for 5 minutes
    async def get_current_price(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get current price quote for ticker."""
        try:
            # yfinance is synchronous, so we're wrapping it
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            last_quote = ticker_obj.history(period="1d").iloc[-1]
            
            return {
                "ticker": ticker,
                "current_price": info.get("currentPrice", last_quote.get("Close")),
                "previous_close": info.get("regularMarketPreviousClose", info.get("previousClose")),
                "change": info.get("regularMarketPrice", 0) - info.get("regularMarketPreviousClose", 0),
                "change_percent": info.get("regularMarketChangePercent", 0) * 100,
                "high": info.get("dayHigh", last_quote.get("High")),
                "low": info.get("dayLow", last_quote.get("Low")),
                "open": info.get("regularMarketOpen", last_quote.get("Open")),
                "volume": info.get("regularMarketVolume", last_quote.get("Volume"))
            }
        except Exception as e:
            self.logger.error(f"Error getting Yahoo Finance price for {ticker}: {e}")
            return None
    
    @cached(ttl=3600)  # Cache for 1 hour
    async def get_historical_data_optimized(self, ticker: str, days_ago: int) -> Optional[Dict[str, Any]]:
        """Get historical price data for analysis."""
        try:
            self.logger.info(f"Getting historical data from Yahoo Finance for {ticker} over {days_ago} days")
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_ago + 5)  # Add buffer days
            
            ticker_obj = yf.Ticker(ticker)
            hist_df = ticker_obj.history(start=start_date.strftime("%Y-%m-%d"), 
                                         end=end_date.strftime("%Y-%m-%d"))
            
            if hist_df.empty or len(hist_df) < 2:
                self.logger.warning(f"Insufficient Yahoo Finance data points for {ticker}")
                return None
                
            # Get the actual start and end dates based on available data
            actual_end_date = hist_df.index[-1].strftime("%Y-%m-%d")
            
            # Find the proper start date (days_ago)
            if len(hist_df) <= days_ago:
                actual_start_date = hist_df.index[0].strftime("%Y-%m-%d")
                start_price = hist_df["Close"].iloc[0]
            else:
                # Find closest date to desired days_ago
                actual_start_date = hist_df.index[-min(days_ago, len(hist_df))].strftime("%Y-%m-%d")
                start_price = hist_df["Close"].iloc[-min(days_ago, len(hist_df))]
            
            end_price = hist_df["Close"].iloc[-1]
            
            # Calculate price change
            price_change = end_price - start_price
            price_change_percent = (price_change / start_price) * 100 if start_price != 0 else 0
            
            # Get high and low in the period
            relevant_df = hist_df.iloc[-min(days_ago, len(hist_df)):]
            period_high = relevant_df["High"].max()
            period_low = relevant_df["Low"].min()
            
            result = {
                "period_description": f"{days_ago} days",
                "start_date": actual_start_date,
                "end_date": actual_end_date,
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "period_high": round(period_high, 2),
                "period_low": round(period_low, 2),
                "data_points": len(relevant_df),
                "data_source": "yahoo_finance"
            }
            
            self.logger.info(f"Successfully calculated historical data via Yahoo Finance for {ticker}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting Yahoo Finance historical data for {ticker}: {e}")
            return None

    @cached(ttl=1800)  # Cache for 30 minutes
    async def get_company_news(self, ticker: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get company news articles."""
        try:
            # yfinance news functionality is limited, but we can get what's available
            ticker_obj = yf.Ticker(ticker)
            news = ticker_obj.news
            
            if not news:
                return []
                
            news_items = []
            for article in news[:10]:  # Limit to 10 most recent
                # Format to match the existing news structure in the app
                published_at = datetime.fromtimestamp(article.get("providerPublishTime", 0))
                
                # Filter by date if needed
                if (datetime.now() - published_at).days > days_back:
                    continue
                    
                news_items.append({
                    "title": article.get("title", ""),
                    "summary": article.get("summary", ""),
                    "source": article.get("publisher", "Yahoo Finance"),
                    "published_at": published_at.isoformat(),  # Convert to ISO string
                    "url": article.get("link", ""),
                    "related": ticker,
                    "sentiment": None  # Will be analyzed by Gemini
                })
                
            return news_items
            
        except Exception as e:
            self.logger.error(f"Error getting Yahoo Finance news for {ticker}: {e}")
            return []