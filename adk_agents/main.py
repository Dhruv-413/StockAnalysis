import asyncio
from typing import Dict, Any, List
from google.adk.agents import SequentialAgent, ParallelAgent, Agent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner

# Import the agent functionality
from .identify_ticker import identify_ticker_agent, identify_ticker_tool, identify_ticker
from .ticker_price import ticker_price_agent, fetch_price_tool, fetch_price
from .ticker_news import ticker_news_agent, fetch_news_tool, fetch_news
from .ticker_price_change import ticker_price_change_agent, calculate_price_change_tool, calculate_price_change
from .ticker_analysis import ticker_analysis_agent, analyze_stock_tool, analyze_stock

# Create a wrapper for fetching data in parallel 
async def fetch_stock_data(ticker: str, days_back: int = 7) -> Dict[str, Any]:
    """
    Fetches price, news, and price change data in parallel
    
    Args:
        ticker: Stock ticker symbol
        days_back: Number of days to look back for historical data and news
        
    Returns:
        Dictionary with price_data, news_data, and price_change_data
    """
    if not ticker:
        return {
            "price_data": {},
            "news_data": {"news_items": []},
            "price_change_data": {}
        }
    
    # Execute in parallel
    price_task = asyncio.create_task(fetch_price(ticker))
    news_task = asyncio.create_task(fetch_news(ticker, days_back))
    price_change_task = asyncio.create_task(calculate_price_change(ticker, days_back))
    
    # Wait for all tasks
    results = await asyncio.gather(price_task, news_task, price_change_task, return_exceptions=True)
    
    # Process results
    price_data = results[0] if not isinstance(results[0], Exception) else {}
    news_data = results[1] if not isinstance(results[1], Exception) else {"news_items": []}
    price_change_data = results[2] if not isinstance(results[2], Exception) else {}
    
    return {
        "price_data": price_data,
        "news_data": news_data,
        "price_change_data": price_change_data
    }

# Create the parallel fetcher tool
parallel_fetch_tool = FunctionTool(fetch_stock_data)

# Create the parallel fetcher agent - removed needs_model attribute
parallel_fetch_agent = Agent(
    name="ParallelFetchAgent",
    tools=[parallel_fetch_tool],
    description="Fetches multiple types of stock data in parallel"
)

# Main function to process a stock query
async def process_stock_query(query: str) -> Dict[str, Any]:
    """
    Process a natural language query about stocks.
    
    Args:
        query: A natural language query about stocks (e.g., "How is Apple doing today?")
        
    Returns:
        A comprehensive analysis of the stock mentioned in the query
    """
    # Step 1: Identify the ticker
    ticker_info = await identify_ticker(query)
    ticker = ticker_info.get("ticker")
    
    if not ticker:
        return {
            "error": "Could not identify a stock ticker from your query",
            "query": query
        }
    
    # Determine appropriate timeframe from query
    timeframe = "recent"
    days_back = 7
    query_lower = query.lower()
    
    if "today" in query_lower:
        timeframe = "today"
        days_back = 1
    elif "week" in query_lower or "7 day" in query_lower:
        timeframe = "7 days"
        days_back = 7
    elif "month" in query_lower or "30 day" in query_lower:
        timeframe = "30 days"
        days_back = 30
        
    # Step 2: Fetch data in parallel
    parallel_data = await fetch_stock_data(ticker, days_back)
    
    # Get the individual data components
    price_data = parallel_data.get("price_data", {})
    news_data = parallel_data.get("news_data", {})
    news_items = news_data.get("news_items", [])
    price_change_data = parallel_data.get("price_change_data", {})
    
    # Step 3: Analyze the stock
    analysis_result = await analyze_stock(
        ticker=ticker,
        price_data=price_data,
        news_items=news_items,
        price_change_data=price_change_data,
        original_query=query,
        timeframe=timeframe,
        intent="general_query"
    )
    
    # Step 4: Prepare final output
    result = {
        "query": query,
        "ticker": ticker,
        "company_name": ticker_info.get("company_name"),
        "current_price": price_data.get("current_price", "N/A"),
        "price_change": price_data.get("change_percent", "N/A"),
        "analysis": analysis_result.get("analysis_summary", f"Analysis for {ticker}"),
        "sentiment": analysis_result.get("sentiment", "neutral"),
        "key_insights": analysis_result.get("key_insights", []),
        "timeframe": timeframe,
        "news_count": len(news_items),
        "top_news": news_items[:3] if news_items else []
    }
    
    if price_change_data:
        result["historical_change"] = {
            "period": price_change_data.get("period", f"{days_back} days"),
            "percent_change": price_change_data.get("change_percent", "N/A"),
            "start_price": price_change_data.get("open", "N/A"),
            "end_price": price_change_data.get("close", "N/A")
        }
    
    return result

# Create the main query processing tool
process_query_tool = FunctionTool(process_stock_query)

# Create the main agent - removed needs_model attribute
stock_analysis_agent = Agent(
    name="StockAnalysisAgent",
    tools=[process_query_tool],
    description="Analyzes stocks based on natural language queries"
)

# For running the workflow
if __name__ == "__main__":
    # Create a runner with the agent
    runner = InMemoryRunner(agent=stock_analysis_agent)
    
    # Example query
    query = "How is Apple stock doing today?"
    
    # Run the workflow by calling the function directly
    import asyncio
    result = asyncio.run(process_stock_query(query))
    
    # Print the result
    print(f"Query: {query}")
    print(f"Result: {result}")
