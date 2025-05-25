import asyncio
from typing import Dict, Any, Optional
from google.adk.tools import FunctionTool
from google.adk.agents import Agent
from src.agents.ticker_price_change_agent import TickerPriceChangeAgent

ticker_price_change_agent_impl = TickerPriceChangeAgent()

async def calculate_price_change(ticker: str, duration_days: int = 7) -> Dict[str, Any]:
    """
    Calculate price change for a ticker over a given duration.
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

calculate_price_change_tool = FunctionTool(calculate_price_change)

# Create ADK agent
ticker_price_change_agent = Agent(
    name="TickerPriceChangeAgent",
    tools=[calculate_price_change_tool],
    description="Calculates and analyzes price changes over time for a stock"
)
