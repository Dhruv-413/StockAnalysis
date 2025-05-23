import asyncio
from typing import Dict, Any, List
from src.agents.ticker_identification_agent import TickerIdentificationAgent
from src.agents.price_agent import PriceAgent # Original name from logs
from src.agents.news_agent import NewsAgent   # Original name from logs
from src.agents.analysis_agent import AnalysisAgent # Original name from logs
from src.models.schemas import AnalysisRequest, AnalysisResult, NewsItem, PriceData
from src.utils.logger import setup_logger
from src.adapters.gemini_adapter import GeminiAdapter

class MainOrchestrator:
    def __init__(self):
        self.logger = setup_logger("MainOrchestrator")
        self.ticker_agent = TickerIdentificationAgent()
        self.price_agent = PriceAgent()
        self.news_agent = NewsAgent()
        self.analysis_agent = AnalysisAgent()  # Added initialization
        self.gemini = GeminiAdapter()
    
    async def process_request(self, request: AnalysisRequest) -> AnalysisResult:
        """Process stock analysis request through agent pipeline"""
        try:
            # Step 1: Extract intent and identify ticker
            intent_data = await self._extract_intent(request)
            
            # Step 2: Identify ticker if not already known
            ticker_data_response = await self._identify_ticker(request, intent_data) # ticker_data_response is AgentResponse
            
            ticker_info = ticker_data_response.data if ticker_data_response and ticker_data_response.success else {}

            if not ticker_info.get("ticker"):
                return AnalysisResult(
                    ticker="UNKNOWN",
                    analysis_summary="Could not identify a valid stock ticker from your query.",
                    key_insights=["Please specify a company name or stock ticker symbol"]
                )
            
            ticker = ticker_info["ticker"]
            company_name = ticker_info.get("company_name")
            company_profile_data = ticker_info.get("profile_data", {}) # Get profile_data
            
            # Step 3: Fetch data in parallel
            price_task = self.price_agent.execute({"ticker": ticker})
            news_task = self.news_agent.execute({"ticker": ticker, "days_back": 7})
            
            price_response, news_response = await asyncio.gather(
                price_task, news_task, return_exceptions=True
            )
            
            # Step 4: Process responses
            price_data_obj = None  # Renamed to avoid conflict with price_data dict
            news_items = []
            
            price_data_dict_for_analysis = {}  # For analysis agent

            if price_response.success and price_response.data:
                # price_response.data now contains high_price_today, low_price_today, open_price_today, volume
                price_data_obj = PriceData(
                    ticker=ticker,
                    current_price=price_response.data.get("current_price", 0),
                    previous_close=price_response.data.get("previous_close", 0),
                    change=price_response.data.get("change", 0),
                    change_percent=price_response.data.get("change_percent", 0),
                    volume=price_response.data.get("volume"), # Get from price_agent response
                    market_cap=company_profile_data.get("market_cap") if company_profile_data else None, # Get from profile
                    high_price_today=price_response.data.get("high_price_today"), # Get from price_agent response
                    low_price_today=price_response.data.get("low_price_today"),   # Get from price_agent response
                    open_price_today=price_response.data.get("open_price_today")  # Get from price_agent response
                )
                price_data_dict_for_analysis = price_response.data
            
            news_items_list_for_analysis = []  # For analysis agent
            if news_response.success and news_response.data:
                news_items = [
                    NewsItem(**item) for item in news_response.data.get("news_items", [])
                ]
                news_items_list_for_analysis = news_response.data.get("news_items", [])
            
            # Step 5: Perform analysis
            analysis_response = await self.analysis_agent.execute({
                "ticker": ticker,
                "price_data": price_data_dict_for_analysis,
                "news_items": news_items_list_for_analysis,
                "timeframe": intent_data.get("timeframe", "recent")
            })
            
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
                confidence_score=confidence_score_val
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return AnalysisResult(
                ticker="ERROR",
                analysis_summary=f"An error occurred while processing your request: {str(e)}",
                key_insights=["Please try again or contact support"]
            )
    
    async def _extract_intent(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract intent from natural language query"""
        if request.query_type == "structured":
            # Try to parse as JSON
            try:
                import json
                return json.loads(request.query)
            except json.JSONDecodeError:
                pass
        
        # Use Gemini to extract intent
        return await self.gemini.extract_intent_and_ticker(request.query)
    
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
