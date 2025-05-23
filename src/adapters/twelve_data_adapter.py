from typing import Dict, Any, Optional, List
from .base_adapter import BaseAdapter
from src.config import settings
from src.utils.cache import cached

class TwelveDataAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            api_key=settings.twelve_data_api_key or "YOUR_TWELVE_DATA_API_KEY_HERE", # Fallback if not in env
            base_url="https://api.twelvedata.com"
        )
        if not settings.twelve_data_api_key:
            self.logger.warning("Twelve Data API key not found in settings. Adapter may not function.")

    def _get_auth_params(self) -> Dict[str, str]:
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
                **kwargs # Additional parameters specific to the indicator
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
            # Common endpoint for time series / OHLCV
            data = await self._make_request("time_series", params)
            return data.get("values") if data and "values" in data else None
        except Exception as e:
            self.logger.error(f"Error getting OHLCV for {symbol} from Twelve Data: {e}")
            return None

# Example usage (for testing, not part of the class)
# async def main():
#     adapter = TwelveDataAdapter()
#     if adapter.api_key and adapter.api_key != "YOUR_TWELVE_DATA_API_KEY_HERE":
#         rsi_data = await adapter.get_technical_indicator("AAPL", "rsi", interval="1day")
#         print("RSI Data:", rsi_data)
#         ohlcv_data = await adapter.get_price_ohlcv("AAPL", interval="1day")
#         print("OHLCV Data:", ohlcv_data)
#     await adapter.close()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
