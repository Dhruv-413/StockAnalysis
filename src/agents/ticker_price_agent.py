from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter
from src.adapters.yahoo_finance_adapter import YahooFinanceAdapter 
from src.adapters.twelve_data_adapter import TwelveDataAdapter

class TickerPriceAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerPriceAgent")
        self.finnhub = FinnhubAdapter()
        self.yahoo = YahooFinanceAdapter()
        self.twelve_data = TwelveDataAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch current price data for ticker with fallbacks to multiple sources"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        
        # Try Finnhub
        self.logger.info(f"Attempting to fetch price data for {ticker} from Finnhub")
        quote_data = await self.finnhub.get_quote(ticker)
        
        # Try Yahoo Finance
        if not quote_data or not quote_data.get("current_price"):
            self.logger.warning(f"Finnhub data unavailable for {ticker}. Trying Yahoo Finance...")
            
            try:
                yahoo_data = await self.yahoo.get_current_price(ticker)
                if yahoo_data and yahoo_data.get("current_price"):
                    self.logger.info(f"Successfully fetched {ticker} price from Yahoo Finance")
                    quote_data = yahoo_data
                    # Add source information
                    quote_data["data_source"] = "yahoo_finance"
            except Exception as e:
                self.logger.error(f"Error getting Yahoo Finance price for {ticker}: {e}")
        
        # Try Twelve Data
        if not quote_data or not quote_data.get("current_price"):
            self.logger.warning(f"Yahoo Finance data unavailable for {ticker}. Trying Twelve Data...")
            
            try:
                twelve_data = await self.twelve_data.get_latest_price(ticker)
                if twelve_data and twelve_data.get("price"):
                    self.logger.info(f"Successfully fetched {ticker} price from Twelve Data")
                    quote_data = {
                        "current_price": twelve_data.get("price"),
                        "previous_close": twelve_data.get("previous_close", None),
                        "change": twelve_data.get("change", None),
                        "change_percent": twelve_data.get("percent_change", None),
                        "high": twelve_data.get("high", None),
                        "low": twelve_data.get("low", None),
                        "open": twelve_data.get("open", None),
                        "data_source": "twelve_data"
                    }
            except Exception as e:
                self.logger.error(f"Error getting Twelve Data price for {ticker}: {e}")
        
        # Raise error
        if not quote_data or not quote_data.get("current_price"):
            raise ValueError(f"Could not fetch price data for {ticker} from any source")
        
        # Set data source if not already set
        if "data_source" not in quote_data:
            quote_data["data_source"] = "finnhub"
            
        return {
            "ticker": ticker,
            "current_price": quote_data.get("current_price"),
            "previous_close": quote_data.get("previous_close"),
            "change": quote_data.get("change"),
            "change_percent": quote_data.get("change_percent"),
            "high_price_today": quote_data.get("high"),
            "low_price_today": quote_data.get("low"),
            "open_price_today": quote_data.get("open"),
            "data_source": quote_data.get("data_source", "unknown"),
            "timestamp": quote_data.get("timestamp")
        }
