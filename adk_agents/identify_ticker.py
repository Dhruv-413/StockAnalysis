import asyncio
from typing import Dict, Any
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

from src.agents.ticker_identification_agent import TickerIdentificationAgent

# Initialize the agent
ticker_identification_agent = TickerIdentificationAgent()

async def identify_ticker(query: str) -> Dict[str, Any]:
    """
    Identify a stock ticker from a natural language query.
    
    Args:
        query: A natural language query about a stock, e.g. "How is Apple doing today?"
        
    Returns:
        A dictionary containing the identified ticker, company name, and confidence score.
    """
    agent_input = {"query": query}
    response = await ticker_identification_agent.execute(agent_input)
    
    if response.success and response.data:
        return {
            "ticker": response.data.get("ticker"),
            "company_name": response.data.get("company_name", "Unknown Company"),
            "confidence": response.data.get("confidence", 0.0)
        }
    else:
        return {
            "ticker": None,
            "company_name": None,
            "confidence": 0.0,
            "error": response.error_message or "Failed to identify ticker"
        }

# Register as ADK Tool
identify_ticker_tool = FunctionTool(
    identify_ticker
)

# Create ADK agent
identify_ticker_agent = Agent(
    name="TickerIdentificationAgent",
    tools=[identify_ticker_tool],
    description="Identifies the stock ticker symbol from a natural language query."
)

# For testing this component directly
if __name__ == "__main__":
    query = "How is Apple stock performing today?"
    result = asyncio.run(identify_ticker(query))
    print(f"Query: {query}")
    print(f"Result: {result}")
