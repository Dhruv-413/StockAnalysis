import asyncio
import re # For parsing timeframe
from typing import Dict, Any, List, Optional # Added Optional
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
        self.gemini_adapter = GeminiAdapter()  # Use Gemini for intent extraction
        self.ticker_agent = TickerIdentificationAgent()
        self.price_agent = TickerPriceAgent()
        self.news_agent = TickerNewsAgent()
        self.analysis_agent = TickerAnalysisAgent()
        self.price_change_agent = TickerPriceChangeAgent()

    def _parse_timeframe_to_days(self, timeframe_str: str) -> Optional[int]:
        """
        Parse a timeframe string into number of days.
        """
        if not timeframe_str:
            return None
        
        timeframe_lower = timeframe_str.lower().strip()
        self.logger.info(f"Parsing timeframe: '{timeframe_lower}'")
        
        # Enhanced parsing for common timeframes
        if "7 days" in timeframe_lower or "seven days" in timeframe_lower:
            return 7
        elif "week" in timeframe_lower or "1 week" in timeframe_lower:
            return 7
        elif "2 weeks" in timeframe_lower or "two weeks" in timeframe_lower:
            return 14
        elif "month" in timeframe_lower or "30 days" in timeframe_lower:
            return 30
        elif "3 months" in timeframe_lower or "quarter" in timeframe_lower:
            return 90
        elif "6 months" in timeframe_lower:
            return 180
        elif "year" in timeframe_lower or "12 months" in timeframe_lower:
            return 365
        elif "today" in timeframe_lower:
            return 1
        elif "yesterday" in timeframe_lower:
            return 2
        
        # Try to extract number + unit
        import re
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
        
        self.logger.warning(f"Could not parse timeframe string '{timeframe_str}' to days.")
        return None

    async def process_request(self, request: AnalysisRequest) -> AnalysisResult:
        """Process stock analysis request through agent pipeline"""
        try:
            self.logger.info(f"=== ORCHESTRATOR START ===")
            self.logger.info(f"Raw user query: '{request.query}'")
            self.logger.info(f"Query type: '{request.query_type}'")
            
            # Step 1: Extract intent and identify ticker
            intent_data = await self._extract_intent(request)
            self.logger.info(f"Extracted intent_data: {intent_data}")
            
            extracted_intent_str = intent_data.get("intent", "general_query")
            
            # Step 2: Identify ticker if not already known
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
            
            # Parse timeframe - use the extracted timeframe, not just default
            timeframe_str = intent_data.get("timeframe", "recent")
            self.logger.info(f"DEBUG: Timeframe from intent: '{timeframe_str}'")
            duration_days = self._parse_timeframe_to_days(timeframe_str)
            
            # For historical analysis, always try to get historical data
            if intent_data.get("intent") == "historical_analysis" and duration_days is None:
                duration_days = 7  # Default for historical queries
                self.logger.info(f"Historical analysis detected, defaulting to {duration_days} days")
            elif duration_days is None:
                duration_days = 7  # General default
                self.logger.info(f"No timeframe parsed, defaulting to {duration_days} days")
            
            self.logger.info(f"DEBUG: Final duration_days: {duration_days}")
            
            price_change_data_for_analysis: Optional[Dict] = None 
            price_change_data_for_result: Optional[PriceChangeData] = None 

            # ALWAYS attempt to get historical data using Alpha Vantage
            self.logger.info(f"DEBUG: Requesting historical price data for {ticker} over {duration_days} days using Alpha Vantage")
            try:
                price_change_agent_response = await self.price_change_agent.execute({
                    "ticker": ticker, 
                    "duration_days": duration_days
                })
                
                self.logger.info(f"DEBUG: Alpha Vantage price change agent response: {price_change_agent_response}")
                
                if price_change_agent_response and price_change_agent_response.success and price_change_agent_response.data:
                    self.logger.info(f"DEBUG: Alpha Vantage historical data SUCCESS: {price_change_agent_response.data}")
                    price_change_data_for_analysis = price_change_agent_response.data
                    try:
                        price_change_data_for_result = PriceChangeData(**price_change_agent_response.data)
                        self.logger.info(f"DEBUG: Created PriceChangeData object successfully from Alpha Vantage")
                    except Exception as e:
                        self.logger.error(f"Failed to parse Alpha Vantage historical data into schema: {e}")
                        price_change_data_for_result = None
                else:
                    self.logger.error(f"Alpha Vantage historical price agent failed: success={price_change_agent_response.success if price_change_agent_response else 'None'}")
            except Exception as e:
                self.logger.error(f"Error executing Alpha Vantage historical price agent: {e}", exc_info=True)

            # Step 3: Fetch data in parallel
            tasks_to_run = {
                "price": self.price_agent.execute({"ticker": ticker}),
                "news": self.news_agent.execute({"ticker": ticker, "days_back": 7})
            }
            
            results = await asyncio.gather(*tasks_to_run.values(), return_exceptions=True)
            
            task_keys = list(tasks_to_run.keys())
            responses: Dict[str, Any] = {task_keys[i]: results[i] for i in range(len(task_keys))}

            # Step 4: Process responses
            price_data_obj: Optional[PriceData] = None
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
            elif isinstance(price_response, Exception):
                 self.logger.error(f"Price agent execution failed: {price_response}")

            news_response = responses.get("news")
            if news_response and not isinstance(news_response, Exception) and news_response.success and news_response.data:
                news_items = [
                    NewsItem(**item) for item in news_response.data.get("news_items", [])
                ]
                news_items_list_for_analysis = news_response.data.get("news_items", [])
            elif isinstance(news_response, Exception):
                self.logger.error(f"News agent execution failed: {news_response}")

            # Step 5: Perform analysis
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
            
            # Debug logging
            self.logger.error(f"DEBUG ORCHESTRATOR: request.query = '{request.query}'")
            self.logger.error(f"DEBUG ORCHESTRATOR: analysis_input['original_query'] = '{analysis_input.get('original_query', 'NOT_FOUND')}'")
            
            self.logger.info(f"Input for AnalysisAgent: {analysis_input}")
            analysis_response = await self.analysis_agent.execute(analysis_input)
            self.logger.info(f"AnalysisAgent response: Success={analysis_response.success}, Data={analysis_response.data}")
            
            # Step 6: Build final result
            analysis_summary_text = "Analysis not available"
            key_insights_list = []
            sentiment_text = None
            confidence_score_val = None

            if analysis_response.success and analysis_response.data:
                analysis_summary_text = analysis_response.data.get("analysis_summary", "Analysis summary not provided.")
                key_insights_list = analysis_response.data.get("key_insights", [])
                sentiment_text = analysis_response.data.get("sentiment")
                confidence_score_val = analysis_response.data.get("confidence_score")

            result = AnalysisResult(
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
            
            self.logger.info(f"DEBUG: Final result price_change_data: {result.price_change_data}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}", exc_info=True)
            return AnalysisResult(
                ticker="ERROR",
                analysis_summary=f"An error occurred while processing your request: {str(e)}",
                key_insights=["Please try again or contact support"]
            )
    
    async def _extract_intent(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract intent and basic information from the request using Gemini"""
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
    
    async def _identify_ticker(self, request: AnalysisRequest, intent_data: Dict[str, Any]) -> Dict[str, Any]: # This returns AgentResponse
        """Identify ticker using the ticker identification agent"""
        input_data = {
            "query": request.query,
            "company_name": intent_data.get("company_name"),
            "ticker": intent_data.get("ticker")
        }
        
        response = await self.ticker_agent.execute(input_data)
        # The orchestrator expects the direct data dict from this helper in the original structure
        # However, the agent returns AgentResponse. We should adapt to what the orchestrator expects or change the orchestrator.
        # For minimal change to the orchestrator's direct use of `ticker_data.get("ticker")` etc.,
        # this helper should return the .data attribute.
        return response # The caller will access response.data
