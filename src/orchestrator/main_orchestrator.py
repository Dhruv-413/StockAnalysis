import asyncio
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from src.agents.ticker_identification_agent import TickerIdentificationAgent
from src.agents.ticker_price_agent import TickerPriceAgent
from src.agents.ticker_news_agent import TickerNewsAgent
from src.agents.ticker_analysis_agent import TickerAnalysisAgent
from src.agents.ticker_price_change_agent import TickerPriceChangeAgent
from src.models.schemas import AnalysisRequest, AnalysisResult, PriceData, NewsItem, PriceChangeData
from src.adapters.gemini_adapter import GeminiAdapter
from src.utils.logger import setup_logger

class MainOrchestrator:
    def __init__(self):
        self.logger = setup_logger("MainOrchestrator")
        
        # Initialize agents
        self.gemini_adapter = GeminiAdapter()
        self.ticker_agent = TickerIdentificationAgent()
        self.price_agent = TickerPriceAgent()
        self.news_agent = TickerNewsAgent()
        self.analysis_agent = TickerAnalysisAgent()
        self.price_change_agent = TickerPriceChangeAgent()

    def _parse_timeframe_to_days(self, timeframe_str: str) -> Optional[int]:
        """Parse timeframe string to number of days"""
        if not timeframe_str:
            return None
        
        timeframe_lower = timeframe_str.lower().strip()
        
        # Common timeframes
        if "7 days" in timeframe_lower or "week" in timeframe_lower:
            return 7
        elif "30 days" in timeframe_lower or "month" in timeframe_lower:
            return 30
        elif "today" in timeframe_lower:
            return 1
        elif "yesterday" in timeframe_lower:
            return 2
        
        # Extract number + unit
        match = re.search(r'(\d+)\s*(day|week|month|year)', timeframe_lower)
        if match:
            number, unit = match.groups()
            number = int(number)
            if unit.startswith('day'):
                return number
            elif unit.startswith('week'):
                return number * 7
            elif unit.startswith('month'):
                return number * 30
            elif unit.startswith('year'):
                return number * 365
        
        return None

    async def process_request(self, request: AnalysisRequest) -> AnalysisResult:
        """Process stock analysis request through agent pipeline"""
        try:
            # Extract intent and identify ticker
            intent_data = await self._extract_intent(request)
            extracted_intent_str = intent_data.get("intent", "general_query")
            
            # Identify ticker
            ticker_data_response = await self._identify_ticker(request, intent_data)
            ticker_info = ticker_data_response.data if ticker_data_response and ticker_data_response.success else {}

            if not ticker_info.get("ticker"):
                return AnalysisResult(
                    ticker="UNKNOWN",
                    analysis_summary="Could not identify a valid stock ticker from your query.",
                    key_insights=["Please specify a company name or stock ticker symbol"]
                )
            
            ticker = ticker_info["ticker"]
            company_name = ticker_info.get("company_name")
            company_profile_data = ticker_info.get("profile_data", {})
            
            # Parse timeframe
            timeframe_str = intent_data.get("timeframe", "recent")
            duration_days = self._parse_timeframe_to_days(timeframe_str)
            
            # Extract from original query if needed
            if duration_days is None:
                query_lower = request.query.lower()
                if "today" in query_lower:
                    duration_days = None
                elif "30 days" in query_lower:
                    duration_days = 30
                elif "7 days" in query_lower:
                    duration_days = 7
                elif "week" in query_lower:
                    duration_days = 7
                elif "month" in query_lower:
                    duration_days = 30
            
            # Default handling
            if intent_data.get("intent") == "historical_analysis" and duration_days is None:
                duration_days = 7
            elif duration_days is None and "today" not in request.query.lower():
                duration_days = 7
            
            price_change_data_for_analysis: Optional[Dict] = None 
            price_change_data_for_result: Optional[PriceChangeData] = None
            price_data_obj: Optional[PriceData] = None

            # Get historical data if needed
            if duration_days and duration_days > 0:
                try:
                    price_change_agent_response = await self.price_change_agent.execute({
                        "ticker": ticker, 
                        "duration_days": duration_days
                    })
                    
                    if price_change_agent_response and price_change_agent_response.success and price_change_agent_response.data:
                        price_change_data_for_analysis = price_change_agent_response.data
                        try:
                            price_change_data_for_result = PriceChangeData(**price_change_agent_response.data)
                        except Exception as e:
                            self.logger.error(f"Failed to parse historical data: {e}")
                            price_change_data_for_result = None
                except Exception as e:
                    self.logger.error(f"Error executing price change agent: {e}")

            # Fetch current data in parallel
            tasks_to_run = {
                "price": self.price_agent.execute({"ticker": ticker}),
                "news": self.news_agent.execute({"ticker": ticker, "days_back": 7})
            }
            
            results = await asyncio.gather(*tasks_to_run.values(), return_exceptions=True)
            task_keys = list(tasks_to_run.keys())
            responses: Dict[str, Any] = {task_keys[i]: results[i] for i in range(len(task_keys))}

            # Process responses
            news_items: List[NewsItem] = []
            price_data_dict_for_analysis: Dict = {}
            news_items_list_for_analysis: List[Dict] = []

            price_response = responses.get("price")
            if price_response and not isinstance(price_response, Exception) and price_response.success and price_response.data:
                price_data_obj = PriceData(
                    ticker=ticker,
                    current_price=price_response.data.get("current_price", 0),
                    previous_close=price_response.data.get("previous_close", 0),
                    change=price_response.data.get("change", 0),
                    change_percent=price_response.data.get("change_percent", 0),
                    volume=price_response.data.get("volume"),
                    market_cap=company_profile_data.get("market_cap") if company_profile_data else None,
                    high_price_today=price_response.data.get("high_price_today"),
                    low_price_today=price_response.data.get("low_price_today"),
                    open_price_today=price_response.data.get("open_price_today")
                )
                price_data_dict_for_analysis = price_response.data

            news_response = responses.get("news")
            if news_response and not isinstance(news_response, Exception) and news_response.success and news_response.data:
                news_items = [
                    NewsItem(**item) for item in news_response.data.get("news_items", [])
                ]
                news_items_list_for_analysis = news_response.data.get("news_items", [])

            # Calculate today's change if no historical data but have current price
            if price_data_obj and not price_change_data_for_result:
                current_price = price_data_obj.current_price
                previous_close = price_data_obj.previous_close
                
                if current_price and previous_close:
                    today_change = current_price - previous_close
                    today_change_percent = (today_change / previous_close) * 100 if previous_close != 0 else 0
                    
                    today_price_change_dict = {
                        "period": "1 day",
                        "open": previous_close,
                        "close": current_price,
                        "change": round(today_change, 2),
                        "change_percent": round(today_change_percent, 2),
                        "high": price_data_obj.high_price_today,
                        "low": price_data_obj.low_price_today,
                        "meta": {
                            "start_date_used": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                            "end_date_used": datetime.now().strftime("%Y-%m-%d"),
                            "data_points": 1,
                            "data_source": "calculated_daily"
                        }
                    }
                    
                    try:
                        price_change_data_for_result = PriceChangeData(**today_price_change_dict)
                        price_change_data_for_analysis = today_price_change_dict
                    except Exception as e:
                        self.logger.error(f"Failed to create calculated PriceChangeData: {e}")

            # Perform analysis
            analysis_input = {
                "ticker": ticker,
                "price_data": price_data_dict_for_analysis,
                "news_items": news_items_list_for_analysis,
                "timeframe": timeframe_str or "recent",
                "intent": extracted_intent_str,
                "original_query": request.query
            }
            if price_change_data_for_analysis: 
                analysis_input["price_change_data"] = price_change_data_for_analysis
            
            analysis_response = await self.analysis_agent.execute(analysis_input)
            
            # Build final result
            analysis_summary_text = "Analysis not available"
            key_insights_list = []
            sentiment_text = None
            confidence_score_val = None

            if analysis_response.success and analysis_response.data:
                analysis_summary_text = analysis_response.data.get("analysis_summary", "Analysis summary not provided.")
                key_insights_list = analysis_response.data.get("key_insights", [])
                sentiment_text = analysis_response.data.get("sentiment")
                confidence_score_val = analysis_response.data.get("confidence_score")

            return AnalysisResult(
                ticker=ticker,
                company_name=company_name,
                analysis_summary=analysis_summary_text,
                price_data=price_data_obj,
                recent_news=news_items,
                key_insights=key_insights_list,
                sentiment=sentiment_text,
                confidence_score=confidence_score_val,
                price_change_data=[price_change_data_for_result] if price_change_data_for_result else None
            )
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return AnalysisResult(
                ticker="ERROR",
                analysis_summary=f"An error occurred while processing your request: {str(e)}",
                key_insights=["Please try again or contact support"]
            )
    
    async def _extract_intent(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract intent using Gemini"""
        try:
            return await self.gemini_adapter.extract_intent_and_ticker(request.query)
        except Exception as e:
            self.logger.error(f"Error extracting intent: {e}")
            return {
                "company_name": None,
                "ticker": None,
                "intent": "general_query",
                "timeframe": "recent"
            }
    
    async def _identify_ticker(self, request: AnalysisRequest, intent_data: Dict[str, Any]):
        """Identify ticker using ticker identification agent"""
        input_data = {
            "query": request.query,
            "company_name": intent_data.get("company_name"),
            "ticker": intent_data.get("ticker")
        }
        
        return await self.ticker_agent.execute(input_data)
