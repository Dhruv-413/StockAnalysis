import asyncio
from typing import Dict, Any, List
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

from src.agents.ticker_news_agent import TickerNewsAgent

# Initialize the agent
ticker_news_agent_impl = TickerNewsAgent()

async def fetch_news(ticker: str, days_back: int = 7) -> Dict[str, Any]:
    """
    Fetch recent news for a stock ticker.
    
    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT)
        days_back: Number of days to look back for news (default: 7)
        
    Returns:
        A dictionary with news items and information
    """
    if not ticker:
        return {"error": "No ticker provided", "news_items": []}
        
    agent_input = {"ticker": ticker, "days_back": days_back}
    response = await ticker_news_agent_impl.execute(agent_input)
    
    if response.success and response.data:
        return response.data
    else:
        return {
            "ticker": ticker,
            "news_count": 0, 
            "news_items": [],
            "error": response.error_message or f"Failed to fetch news for {ticker}"
        }

# Register as ADK Tool
fetch_news_tool = FunctionTool(fetch_news)

# Create ADK agent - removed needs_model attribute
ticker_news_agent = Agent(
    name="TickerNewsAgent",
    tools=[fetch_news_tool],
    description="Fetches and aggregates recent news for a stock ticker"
)

# For testing this component directly
if __name__ == "__main__":
    ticker = "AAPL"
    result = asyncio.run(fetch_news(ticker))
    print(f"Ticker: {ticker}")
    print(f"News Count: {result.get('news_count', 0)}")
    for news in result.get('news_items', [])[:2]:  # Show first two news items
        print(f"- {news.get('title')}")
