from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter

class TickerPriceAgent(BaseAgent): # Renamed class
    def __init__(self):
        super().__init__("TickerPriceAgent") # Renamed agent name
        self.finnhub = FinnhubAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch current price data for ticker"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        quote_data = await self.finnhub.get_quote(ticker)
        
        if not quote_data:
            raise ValueError(f"Could not fetch price data for {ticker}")
        
        # Finnhub quote data keys: c, pc, d, dp, h, l, o, t (timestamp)
        # current_price (c), previous_close (pc), change (d), change_percent (dp)
        # high (h), low (l), open (o), volume (v - not directly in quote, but often requested)
        # For volume, we might need another call or it might be part of a different dataset.
        # The existing PriceData schema expects 'volume'. Finnhub's quote doesn't directly provide 'v' for volume.
        # Let's assume for now it's part of the quote or can be fetched separately if needed.
        # The provided quote_data from finnhub.get_quote already maps to the expected fields.
        
        return {
            "ticker": ticker,
            "current_price": quote_data.get("current_price"),
            "previous_close": quote_data.get("previous_close"),
            "change": quote_data.get("change"),
            "change_percent": quote_data.get("change_percent"),
            "high_price_today": quote_data.get("high"), # h
            "low_price_today": quote_data.get("low"),   # l
            "open_price_today": quote_data.get("open"), # o
            # "volume": quote_data.get("volume") # 'v' is not in quote, usually in candles/timeseries
            # For consistency with existing PriceData, we might need to adjust how volume is sourced.
            # The original PriceAgent returned 'volume'. Let's check FinnhubAdapter.get_quote
            # The adapter's get_quote maps 't' (timestamp of last trade) to volume, which is incorrect.
            # Correcting this: Finnhub's /quote does not return volume.
            # Volume is typically part of daily candles or more detailed time series.
            # For now, we'll return what /quote provides.
            # The schema PriceData has volume as optional.
        }
