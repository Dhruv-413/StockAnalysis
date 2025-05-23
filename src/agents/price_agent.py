from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter

class PriceAgent(BaseAgent):
    def __init__(self):
        super().__init__("PriceAgent")
        self.finnhub = FinnhubAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch current price data for ticker"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        quote_data = await self.finnhub.get_quote(ticker) # This calls the adapter
        
        if not quote_data:
            raise ValueError(f"Could not fetch price data for {ticker}")
        
        # quote_data from adapter is expected to have keys:
        # "current_price", "previous_close", "change", "change_percent",
        # "high", "low", "open", "volume" (volume might be null from /quote)
        return {
            "ticker": ticker,
            "current_price": quote_data.get("current_price"),
            "previous_close": quote_data.get("previous_close"),
            "change": quote_data.get("change"),
            "change_percent": quote_data.get("change_percent"),
            "high_price_today": quote_data.get("high"), # Map from adapter's "high"
            "low_price_today": quote_data.get("low"),   # Map from adapter's "low"
            "open_price_today": quote_data.get("open"), # Map from adapter's "open"
            "volume": quote_data.get("volume")          # Pass through volume
        }
