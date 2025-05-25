from typing import Dict, Any, Optional, List
from .base_adapter import BaseAdapter
from src.config import settings
from ..utils.cache import cached
import httpx

class TwelveDataAdapter(BaseAdapter):
    def __init__(self):
        api_key = settings.twelve_data_api_key
        if not api_key or api_key == "YOUR_TWELVE_DATA_API_KEY_HERE":
            self.logger.warning("Twelve Data API key is not properly configured. Adapter functionality will be limited.")
        
        super().__init__(
            api_key=api_key or "DUMMY_KEY_IF_NONE",
            base_url="https://api.twelvedata.com"
        )
        if not api_key or api_key == "YOUR_TWELVE_DATA_API_KEY_HERE":
            self.api_key = None
            
    def _get_auth_params(self) -> Dict[str, str]:
        if not self.api_key:
            return {}
        return {"apikey": self.api_key}

    @cached(ttl=300) # Cache for 5 minutes
    async def get_technical_indicator(
        self, 
        symbol: str, 
        indicator: str, 
        interval: str = "1day", 
        outputsize: int = 30,
        **kwargs: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch technical indicator data.
        Example indicators: sma, ema, rsi, macd, bbands
        """
        if not self.api_key or self.api_key == "YOUR_TWELVE_DATA_API_KEY_HERE":
            self.logger.error(f"Twelve Data API key not configured. Cannot fetch {indicator} for {symbol}.")
            return None
        try:
            params = {
                "symbol": symbol,
                "interval": interval,
                "outputsize": outputsize,
                **kwargs 
            }
            # The endpoint for indicators is usually the indicator name itself
            data = await self._make_request(indicator.lower(), params)
            return data
        except Exception as e:
            self.logger.error(f"Error getting {indicator} for {symbol} from Twelve Data: {e}")
            return None

    @cached(ttl=300)
    async def get_price_ohlcv(
        self,
        symbol: str,
        interval: str = "1day",
        outputsize: int = 30
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch OHLCV data for a symbol."""
        if not self.api_key or self.api_key == "YOUR_TWELVE_DATA_API_KEY_HERE":
            self.logger.error(f"Twelve Data API key not configured. Cannot fetch OHLCV for {symbol}.")
            return None
        try:
            params = {
                "symbol": symbol,
                "interval": interval,
                "outputsize": outputsize,
            }
            # Common endpoint for time series
            data = await self._make_request("time_series", params)
            return data.get("values") if data and "values" in data else None
        except Exception as e:
            self.logger.error(f"Error getting OHLCV for {symbol} from Twelve Data: {e}")
            return None
        
    @cached(ttl=3600) # Cache for 1 hour
    async def get_historical_data_optimized(
        self, 
        ticker: str, 
        days_ago: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get historical data for price change analysis, similar to Alpha Vantage's implementation.
        
        Args:
            ticker: The stock symbol
            days_ago: How many days to look back
            
        Returns:
            Dictionary with price change information in a consistent format
        """
        self.logger.info(f"Getting optimized historical data from Twelve Data for {ticker} over {days_ago} days")
        
        if days_ago <= 0:
            return None
            
        if not self.api_key or self.api_key == "YOUR_TWELVE_DATA_API_KEY_HERE":
            self.logger.error(f"Twelve Data API key not properly configured. Cannot get historical data for {ticker}.")
            return None
        
        try:
            # For Twelve Data, we need to request enough data points to cover the period
            outputsize = days_ago + 10
            
            # Fetch OHLCV data
            values = await self.get_price_ohlcv(ticker, "1day", outputsize)
            if not values or len(values) < 2:
                self.logger.warning(f"Insufficient data points from Twelve Data for {ticker}")
                return None
                
            # Twelve Data returns data in reverse chronological order (newest first)
            sorted_values = sorted(values, key=lambda x: x.get("datetime", ""))
            
            # Get start and end prices
            if len(sorted_values) <= days_ago:
                start_price = float(sorted_values[0].get("close", 0))
                start_date = sorted_values[0].get("datetime", "").split()[0]  # Get date part only
            else:
                start_idx = max(0, len(sorted_values) - days_ago - 1)
                start_price = float(sorted_values[start_idx].get("close", 0))
                start_date = sorted_values[start_idx].get("datetime", "").split()[0]
                
            # End price is the most recent
            end_price = float(sorted_values[-1].get("close", 0))
            end_date = sorted_values[-1].get("datetime", "").split()[0]
            
            # Calculate price change
            price_change = end_price - start_price
            price_change_percent = (price_change / start_price) * 100 if start_price != 0 else 0
            
            # Find highest and lowest prices in the period
            relevant_values = sorted_values[-days_ago:] if len(sorted_values) > days_ago else sorted_values
            highs = [float(val.get("high", 0)) for val in relevant_values]
            lows = [float(val.get("low", 0)) for val in relevant_values]
            
            period_high = max(highs) if highs else end_price
            period_low = min(lows) if lows else end_price
            
            # Format result to match Alpha Vantage's output format
            result = {
                "period_description": f"{days_ago} days",
                "start_date": start_date,
                "end_date": end_date,
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "period_high": round(period_high, 2),
                "period_low": round(period_low, 2),
                "data_points": len(relevant_values),
                "data_source": "twelve_data"
            }
            
            self.logger.info(f"Successfully calculated historical data via Twelve Data for {ticker}: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in Twelve Data historical data for {ticker}: {e}")
            return None
        
    @cached(ttl=300)  # Cache for 5 minutes
    async def get_latest_price(
        self, ticker: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get latest price quote for a ticker
        
        Args:
            ticker: The stock symbol
            
        Returns:
            Dictionary with current price information
        """
        if not self.api_key:
            self.logger.error("Twelve Data API key not configured properly")
            return None
            
        try:
            url = f"{self.base_url}/quote"
            params = {
                "symbol": ticker,
                "interval": "1day",
                "apikey": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
            if not data or "close" not in data:
                self.logger.warning(f"No price data returned from Twelve Data for {ticker}")
                return None
                
            # Calculate change and percent change
            close_price = float(data.get("close", 0))
            previous_close = float(data.get("previous_close", 0))
            change = close_price - previous_close
            percent_change = (change / previous_close * 100) if previous_close else 0
            
            return {
                "price": close_price,
                "previous_close": previous_close,
                "change": round(change, 2),
                "percent_change": round(percent_change, 2),
                "high": float(data.get("high", 0)),
                "low": float(data.get("low", 0)),
                "open": float(data.get("open", 0)),
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            self.logger.error(f"Error fetching latest price from Twelve Data for {ticker}: {e}")
            return None