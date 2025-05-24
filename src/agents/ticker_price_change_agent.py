from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from src.adapters.alpha_vantage_adapter import AlphaVantageAdapter
from src.models.schemas import PriceChangeData

class TickerPriceChangeAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerPriceChangeAgent")
        self.alpha_vantage_adapter = AlphaVantageAdapter()

    async def _execute_logic(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calculate price change for a ticker over a given duration using Alpha Vantage historical data.
        """
        self.logger.info(f"DEBUG: TickerPriceChangeAgent executing with input: {input_data}")
        self.validate_input(input_data, ["ticker", "duration_days"])
        
        ticker: str = input_data["ticker"]
        duration_days: Any = input_data["duration_days"]

        if not isinstance(duration_days, int) or duration_days <= 0:
            self.logger.error(f"Invalid duration_days: '{duration_days}' for ticker {ticker}")
            return None

        self.logger.info(f"DEBUG: Fetching historical data for {ticker} over {duration_days} days using Alpha Vantage")
        
        try:
            # Use Alpha Vantage's historical data method
            historical_data = await self.alpha_vantage_adapter.get_historical_data_optimized(
                ticker=ticker,
                days_ago=duration_days
            )
            
            self.logger.info(f"DEBUG: Alpha Vantage historical data response: {historical_data}")

            if not historical_data:
                self.logger.error(f"No historical data from Alpha Vantage for {ticker} for {duration_days} days")
                return None
            
            self.logger.info(f"DEBUG: Historical data received: {historical_data}")
            
            result_dict = {
                "period": historical_data.get("period_description"), 
                "open": historical_data.get("start_price"), 
                "close": historical_data.get("end_price"),  
                "change": historical_data.get("price_change"), 
                "change_percent": historical_data.get("price_change_percent"),
                "high": historical_data.get("period_high"),
                "low": historical_data.get("period_low"),
                "meta": { 
                    "start_date_used": historical_data.get("start_date"),
                    "end_date_used": historical_data.get("end_date"),
                    "data_points": historical_data.get("data_points"),
                    "data_source": "alpha_vantage"
                }
            }
            
            # Validate essential fields
            if result_dict["open"] is None or result_dict["close"] is None:
                self.logger.error(f"Essential price data missing for {ticker}: {result_dict}")
                return None

            self.logger.info(f"DEBUG: Final result dict: {result_dict}")
            return result_dict
            
        except Exception as e:
            self.logger.error(f"Error getting historical data for {ticker}: {e}", exc_info=True)
            return None

