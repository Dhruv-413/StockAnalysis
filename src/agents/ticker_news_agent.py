import logging
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter
from src.adapters.marketaux_adapter import MarketauxAdapter
from src.adapters.yahoo_finance_adapter import YahooFinanceAdapter
from src.utils.json_utils import serialize_object

class TickerNewsAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerNewsAgent")
        self.finnhub = FinnhubAdapter()
        self.marketaux = MarketauxAdapter()
        self.yahoo = YahooFinanceAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch recent news for ticker from multiple sources"""
        self.validate_input(input_data, ["ticker"])
        
        ticker = input_data["ticker"]
        days_back = input_data.get("days_back", 7)
        
        # Attempt to get news from all sources in parallel
        import asyncio
        finnhub_task = asyncio.create_task(self.finnhub.get_company_news(ticker, days_back))
        marketaux_task = asyncio.create_task(self.marketaux.get_company_news(ticker, days_back))
        yahoo_task = asyncio.create_task(self.yahoo.get_company_news(ticker, days_back))

        results = await asyncio.gather(finnhub_task, marketaux_task, yahoo_task, return_exceptions=True)
        
        news_items = []
        
        # Process each news source's results
        for i, result in enumerate(results):
            if not isinstance(result, list):
                continue
                
            source_name = ["finnhub", "marketaux", "yahoo"][i]
            for item in result:
                item["source_api"] = source_name
                news_items.append(item)
        
        # Remove duplicates
        deduplicated_news = self._deduplicate_news_items(news_items)
        
        # Create response
        result = {
            "ticker": ticker,
            "news_count": len(deduplicated_news),
            "news_items": deduplicated_news[:15],
            "timeframe_days": days_back,
            "sources_used": self._get_sources_used(results)
        }
        
        # Make sure all datetime objects are serialized to strings
        return serialize_object(result)
    
    def _deduplicate_news_items(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate news based on title similarity"""
        if not news_items:
            return []
            
        # Sort by recency first - ensure we're comparing strings
        sorted_news = sorted(
            news_items, 
            key=lambda x: x.get("published_at", ""), 
            reverse=True
        )
        
        unique_news = []
        titles_seen = set()
        
        for item in sorted_news:
            title = item.get("title", "").lower()
            # Create a simplified version of the title for comparison
            simple_title = ''.join(c for c in title if c.isalnum()).lower()
            
            # Check if we've seen a similar title
            is_duplicate = False
            for seen_title in titles_seen:
                # If 80% of the simplified title matches, consider it a duplicate
                if len(simple_title) > 15 and (
                    simple_title in seen_title or seen_title in simple_title or
                    self._similarity_score(simple_title, seen_title) > 0.8
                ):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                titles_seen.add(simple_title)
                unique_news.append(item)
                
        return unique_news
        
    def _similarity_score(self, str1: str, str2: str) -> float:
        """Calculate simple similarity between two strings"""
        if not str1 or not str2:
            return 0
            
        matches = sum(c1 == c2 for c1, c2 in zip(str1, str2))
        return matches / max(len(str1), len(str2))
    
    def _get_sources_used(self, results: list) -> List[str]:
        """Get list of successful news sources"""
        sources = []
        if isinstance(results[0], list) and results[0]:
            sources.append("finnhub")
        if isinstance(results[1], list) and results[1]:
            sources.append("marketaux") 
        if isinstance(results[2], list) and results[2]:
            sources.append("yahoo")
        return sources
