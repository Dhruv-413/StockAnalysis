from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from src.adapters.gemini_adapter import GeminiAdapter

class TickerAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerAnalysisAgent")
        self.gemini = GeminiAdapter()

    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform analysis using Gemini"""
        self.validate_input(input_data, ["ticker", "price_data", "news_items"])

        ticker = input_data["ticker"]
        price_data_dict = input_data["price_data"] if isinstance(input_data["price_data"], dict) else {}
        news_items_list = input_data["news_items"] if isinstance(input_data["news_items"], list) else []
        
        timeframe = input_data.get("timeframe", "recent")
        intent = input_data.get("intent", "general_query")
        original_query = input_data.get("original_query", "")
        price_change_data_dict: Optional[Dict[str, Any]] = input_data.get("price_change_data")

        analysis_result = await self.gemini.analyze_stock_movement(
            ticker=ticker,
            price_data=price_data_dict,
            news_items=news_items_list,
            timeframe=timeframe,
            intent=intent,
            original_query=original_query,
            price_change_data=price_change_data_dict
        )
        return analysis_result