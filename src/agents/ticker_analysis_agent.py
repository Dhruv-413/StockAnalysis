from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.gemini_adapter import GeminiAdapter

class TickerAnalysisAgent(BaseAgent):  # Renamed class
    def __init__(self):
        super().__init__("TickerAnalysisAgent")  # Renamed agent name
        self.gemini = GeminiAdapter()

    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform analysis using Gemini based on ticker, price data, and news items.
        """
        self.validate_input(input_data, ["ticker", "price_data", "news_items"])

        ticker = input_data["ticker"]
        # Ensure price_data and news_items are in the format expected by GeminiAdapter
        price_data_dict = input_data["price_data"] if isinstance(input_data["price_data"], dict) else {}
        news_items_list = input_data["news_items"] if isinstance(input_data["news_items"], list) else []
        
        timeframe = input_data.get("timeframe", "recent")

        analysis_result = await self.gemini.analyze_stock_movement(
            ticker=ticker,
            price_data=price_data_dict,
            news_items=news_items_list,
            timeframe=timeframe
        )
        return analysis_result