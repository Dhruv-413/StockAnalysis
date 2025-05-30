import asyncio
from typing import Dict, Any, List
from datetime import datetime
from google.adk.tools import FunctionTool
from google.adk.agents import Agent
from src.agents.ticker_news_agent import TickerNewsAgent

ticker_news_agent_impl = TickerNewsAgent()

def serialize_datetime_objects(obj):
    """Convert any datetime objects to ISO format strings to ensure JSON serialization works."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serialize_datetime_objects(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime_objects(item) for item in obj]
    else:
        return obj

async def fetch_news(ticker: str, days_back: int = 7) -> Dict[str, Any]:
    """
    Fetch recent news for a ticker symbol
    """
    try:
        result = await ticker_news_agent_impl.execute({
            "ticker": ticker,
            "days_back": days_back
        })
        
        if result and result.success:
            serialized_data = serialize_datetime_objects(result.data)
            return serialized_data
        else:
            return {
                "ticker": ticker,
                "news_count": 0,
                "news_items": [],
                "timeframe_days": days_back,
                "sources_used": []
            }
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return {
            "ticker": ticker,
            "news_count": 0,
            "news_items": [],
            "timeframe_days": days_back,
            "error": str(e),
            "sources_used": []
        }

fetch_news_tool = FunctionTool(fetch_news)

# Create ADK agent
ticker_news_agent = Agent(
    name="TickerNewsAgent",
    tools=[fetch_news_tool],
    description="Fetches and aggregates recent news for a stock ticker"
)
