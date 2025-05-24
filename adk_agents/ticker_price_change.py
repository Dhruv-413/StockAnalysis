import asyncio
from typing import Dict, Any, Optional
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

from src.agents.ticker_price_change_agent import TickerPriceChangeAgent

# Initialize the agent
ticker_price_change_agent_impl = TickerPriceChangeAgent()

async def calculate_price_change(ticker: str, duration_days: int = 7) -> Dict[str, Any]:
    """
    Calculate price change for a ticker over a given duration.
    
    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT)
        duration_days: Number of days to analyze price change (default: 7)
        
    Returns:
        A dictionary with price change information
    """
    if not ticker:
        return {"error": "No ticker provided"}
        
    agent_input = {"ticker": ticker, "duration_days": duration_days}
    response = await ticker_price_change_agent_impl.execute(agent_input)
    
    if response.success and response.data:
        return response.data
    else:
        return {
            "ticker": ticker,
            "period": f"{duration_days} days",
            "error": response.error_message or f"Failed to calculate price change for {ticker}"
        }

# Register as ADK Tool
calculate_price_change_tool = FunctionTool(calculate_price_change)

# Create ADK agent - removed needs_model attribute
ticker_price_change_agent = Agent(
    name="TickerPriceChangeAgent",
    tools=[calculate_price_change_tool],
    description="Calculates and analyzes price changes over time for a stock"
)

# For testing this component directly
if __name__ == "__main__":
    ticker = "AAPL"
    days = 7
    result = asyncio.run(calculate_price_change(ticker, days))
    print(f"Ticker: {ticker}, Period: {days} days")
    print(f"Result: {result}")
