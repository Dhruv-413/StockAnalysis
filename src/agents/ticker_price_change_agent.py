import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from src.adapters.alpha_vantage_adapter import AlphaVantageAdapter
from src.adapters.twelve_data_adapter import TwelveDataAdapter
from src.adapters.yahoo_finance_adapter import YahooFinanceAdapter

class TickerPriceChangeAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerPriceChangeAgent")
        self.alpha_vantage_adapter = AlphaVantageAdapter()
        self.twelve_data_adapter = TwelveDataAdapter()
        self.yahoo_finance_adapter = YahooFinanceAdapter()
        
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calculate price change for a ticker over a given duration using historical data.
        Uses multiple data sources with automatic fallback.
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
            # Try Alpha Vantage
            historical_data = await self.alpha_vantage_adapter.get_historical_data_optimized(
                ticker=ticker,
                days_ago=duration_days
            )
            
            self.logger.info(f"DEBUG: Alpha Vantage historical data response: {historical_data}")

            # Try Twelve Data
            if not historical_data:
                self.logger.warning(f"Alpha Vantage data unavailable for {ticker}. Trying Twelve Data as backup...")
                
                historical_data = await self.twelve_data_adapter.get_historical_data_optimized(
                    ticker=ticker,
                    days_ago=duration_days
                )
                
                # Try Yahoo Finance
                if not historical_data:
                    self.logger.warning(f"Twelve Data unavailable for {ticker}. Trying Yahoo Finance as backup...")
                    
                    historical_data = await self.yahoo_finance_adapter.get_historical_data_optimized(
                        ticker=ticker,
                        days_ago=duration_days
                    )
                    
                    if not historical_data:
                        self.logger.error(f"No historical data available from any source for {ticker} for {duration_days} days")
                        return None
            
            self.logger.info(f"DEBUG: Historical data received: {historical_data}")
            
            # Process data into standard format
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
                    "data_source": historical_data.get("data_source", "unknown")
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

