import asyncio
from typing import Dict, Any, List, Optional
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

from src.agents.ticker_analysis_agent import TickerAnalysisAgent

# Initialize the agent
ticker_analysis_agent_impl = TickerAnalysisAgent()

async def analyze_stock(
    ticker: str,
    price_data: Dict[str, Any],
    news_items: List[Dict[str, Any]],
    price_change_data: Optional[Dict[str, Any]] = None,
    original_query: str = "",
    timeframe: str = "recent",
    intent: str = "general_query"
) -> Dict[str, Any]:
    """
    Analyze stock data using price, news, and historical information.
    
    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT)
        price_data: Current price information
        news_items: List of news article data
        price_change_data: Historical price change data (optional)
        original_query: The original user query (optional)
        timeframe: Time period for analysis (e.g., "recent", "7 days", etc.)
        intent: Purpose of analysis (e.g., "general_query", "price_check", etc.)
        
    Returns:
        A dictionary with analysis results
    """
    if not ticker:
        return {"error": "No ticker provided", "analysis_summary": "Missing ticker symbol"}
        
    agent_input = {
        "ticker": ticker,
        "price_data": price_data,
        "news_items": news_items,
        "original_query": original_query,
        "timeframe": timeframe,
        "intent": intent
    }
    
    if price_change_data:
        agent_input["price_change_data"] = price_change_data
        
    response = await ticker_analysis_agent_impl.execute(agent_input)
    
    if response.success and response.data:
        return response.data
    else:
        return {
            "analysis_summary": f"Failed to analyze {ticker}",
            "key_insights": [],
            "sentiment": "neutral",
            "confidence_score": 0.0,
            "error": response.error_message or "Analysis error"
        }

# Register as ADK Tool
analyze_stock_tool = FunctionTool(analyze_stock)

# Create ADK agent - removed needs_model attribute
ticker_analysis_agent = Agent(
    name="TickerAnalysisAgent",
    tools=[analyze_stock_tool],
    description="Performs comprehensive analysis of stock performance and generates insights"
)

# For testing this component directly
if __name__ == "__main__":
    ticker = "AAPL"
    price_data = {"ticker": "AAPL", "current_price": 180.25, "change_percent": -1.2}
    news_items = [{"title": "Apple announces new iPhone", "summary": "Apple's latest release..."}]
    result = asyncio.run(analyze_stock(ticker, price_data, news_items))
    print(f"Ticker: {ticker}")
    print(f"Analysis: {result.get('analysis_summary')}")
