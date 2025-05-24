import asyncio
from typing import Dict, Any
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

from src.agents.ticker_price_agent import TickerPriceAgent

# Initialize the agent
ticker_price_agent_impl = TickerPriceAgent()

async def fetch_price(ticker: str) -> Dict[str, Any]:
    """
    Fetch the current price data for a stock ticker.
    
    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        A dictionary with price information including current price, change, etc.
    """
    if not ticker:
        return {"error": "No ticker provided"}
        
    agent_input = {"ticker": ticker}
    response = await ticker_price_agent_impl.execute(agent_input)
    
    if response.success and response.data:
        return response.data
    else:
        return {
            "ticker": ticker,
            "error": response.error_message or f"Failed to fetch price data for {ticker}"
        }

# Register as ADK Tool
fetch_price_tool = FunctionTool(fetch_price)

# Create ADK agent - removed needs_model attribute
ticker_price_agent = Agent(
    name="TickerPriceAgent",
    tools=[fetch_price_tool],
    description="Fetches the current price and related data for a stock"
)

# For testing this component directly
if __name__ == "__main__":
    ticker = "AAPL"
    result = asyncio.run(fetch_price(ticker))
    print(f"Ticker: {ticker}")
    print(f"Result: {result}")
