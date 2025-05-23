from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter

class TickerNewsAgent(BaseAgent): # Renamed class
    def __init__(self):
        super().__init__("TickerNewsAgent") # Renamed agent name
        self.finnhub = FinnhubAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch recent news for ticker"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        days_back = input_data.get("days_back", 7)
        
        news_items = await self.finnhub.get_company_news(ticker, days_back)
        
        return {
            "ticker": ticker,
            "news_count": len(news_items),
            "news_items": news_items, # This is already a list of dicts
            "timeframe_days": days_back
        }
