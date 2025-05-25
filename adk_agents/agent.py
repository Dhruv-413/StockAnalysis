from typing import ClassVar
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from adk_agents.identify_ticker import identify_ticker
from adk_agents.ticker_price import fetch_price
from adk_agents.ticker_news import fetch_news
from adk_agents.ticker_price_change import calculate_price_change
from adk_agents.ticker_analysis import analyze_stock
from adk_agents.main import process_stock_query

class StockAnalysisAgent(Agent):
    root_agent: ClassVar[bool] = True
    
    def __init__(self):
        super().__init__(
            name="StockAnalysisAgent",
            model="gemini-1.5-flash",
            tools=[
                FunctionTool(identify_ticker),
                FunctionTool(fetch_price),
                FunctionTool(fetch_news),
                FunctionTool(calculate_price_change),
                FunctionTool(analyze_stock),
                FunctionTool(process_stock_query)
            ],
            description="Analyzes stocks using natural language queries and provides comprehensive insights"
        )

agent = StockAnalysisAgent()
root_agent = agent
