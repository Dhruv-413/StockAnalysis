from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter

class TickerPriceAgent(BaseAgent): 
    def __init__(self):
        super().__init__("TickerPriceAgent") 
        self.finnhub = FinnhubAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch current price data for ticker"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        quote_data = await self.finnhub.get_quote(ticker)
        
        if not quote_data:
            raise ValueError(f"Could not fetch price data for {ticker}")
 
        return {
            "ticker": ticker,
            "current_price": quote_data.get("current_price"),
            "previous_close": quote_data.get("previous_close"),
            "change": quote_data.get("change"),
            "change_percent": quote_data.get("change_percent"),
            "high_price_today": quote_data.get("high"), # h
            "low_price_today": quote_data.get("low"),   # l
            "open_price_today": quote_data.get("open"), # o
        }
