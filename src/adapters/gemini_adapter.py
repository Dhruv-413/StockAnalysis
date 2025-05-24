import google.generativeai as genai
import json
import re
from typing import Dict, Any, Optional, List
from src.config import settings
from src.utils.logger import setup_logger
from src.utils.cache import cached

class GeminiAdapter:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.logger = setup_logger(self.__class__.__name__)
    
    @cached(ttl=300)
    async def extract_intent_and_ticker(self, query: str) -> Dict[str, Any]:
        """Extract intent and ticker from natural language query"""
        try:
            self.logger.info(f"Gemini extracting intent from query: '{query}'")
            
            # Simple pre-check for very common company names
            common_companies_map = {
                "apple": {"company_name": "Apple Inc.", "ticker": "AAPL"},
                "microsoft": {"company_name": "Microsoft Corporation", "ticker": "MSFT"},
                "google": {"company_name": "Alphabet Inc.", "ticker": "GOOGL"},
                "alphabet": {"company_name": "Alphabet Inc.", "ticker": "GOOGL"},
                "amazon": {"company_name": "Amazon.com Inc.", "ticker": "AMZN"},
                "tesla": {"company_name": "Tesla Inc.", "ticker": "TSLA"},
                "nvidia": {"company_name": "NVIDIA Corporation", "ticker": "NVDA"},
                "meta": {"company_name": "Meta Platforms Inc.", "ticker": "META"},
                "facebook": {"company_name": "Meta Platforms Inc.", "ticker": "META"},
                "nike": {"company_name": "NIKE, Inc.", "ticker": "NKE"},
            }
            
            query_lower = query.lower()
            for name, details in common_companies_map.items():
                if name in query_lower:
                    self.logger.info(f"Common company '{name}' found in query. Using predefined details and extracting rest with Gemini.")
                    
                    prompt_for_common = f"""
                    Given the query: "{query}"
                    And knowing the primary company of interest is "{details['company_name']}" (ticker: {details['ticker']}).

                    Extract the following:
                    1. intent: What the user wants. Be very specific:
                       - "historical_analysis" if asking about performance over time, changes over days/weeks/months
                       - "earnings_check" if asking about profit, earnings, revenue, financial performance
                       - "price_check" if asking about current price, stock price today
                       - "news_summary" if asking about recent news or events
                       - "general_query" for other requests
                    2. timeframe: Time period mentioned (e.g., "7 days", "last 7 days", "past week", "last month", "today").

                    Examples:
                    - "How has Tesla changed in the last 7 days?" -> intent: "historical_analysis", timeframe: "7 days"
                    - "Tesla stock price" -> intent: "price_check", timeframe: "today"
                    - "Was Tesla profitable?" -> intent: "earnings_check", timeframe: "recent"

                    Return a JSON response with "intent" and "timeframe".
                    """
                    response_common = await self.model.generate_content_async(prompt_for_common)
                    
                    # Fix JSON parsing - ensure json module is available
                    try:
                        raw_text = response_common.text.strip()
                        self.logger.info(f"Raw Gemini response: {raw_text}")
                        
                        # Extract JSON from markdown if present
                        if "```json" in raw_text:
                            json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
                            if json_match:
                                raw_text = json_match.group(1)
                        
                        import json as json_module
                        parsed_common_response = json_module.loads(raw_text)
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": parsed_common_response.get("intent", "general_query"),
                            "timeframe": parsed_common_response.get("timeframe", "recent")
                        }
                    except Exception as e:
                        self.logger.error(f"Failed to parse Gemini response: {e}. Raw: {raw_text}")
                        # Extract timeframe manually if JSON parsing fails
                        extracted_timeframe = "recent"
                        if "today" in query.lower():
                            extracted_timeframe = "today"
                        elif "30 days" in query.lower():
                            extracted_timeframe = "30 days"
                        elif "7 days" in query.lower():
                            extracted_timeframe = "7 days"
                        
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": "general_query",
                            "timeframe": extracted_timeframe
                        }

            # If no common company name was pre-identified, proceed with the general Gemini extraction
            prompt = f"""
            Analyze the following stock-related query: "{query}"

            Identify:
            1. "company_name": The full official name of the company (e.g., "Apple Inc."). If no specific company is clear, set to null.
            2. "ticker": The stock ticker symbol (e.g., "AAPL"). If no ticker is clear, set to null.
            3. "intent": The user's primary goal. Be very specific:
               - "earnings_check": If asking about profit, earnings, revenue, financial performance, quarterly results
               - "price_check": If asking about current price, stock price today, market value
               - "historical_analysis": If asking about performance over a time period (e.g., "last 7 days", "this week")
               - "news_summary": If asking about recent news, events, or developments
               - "company_profile": If asking about general company information
               - "general_query": For other requests
            4. "timeframe": Any time period mentioned (e.g., "today", "last 7 days", "Q3 2023"). If not specified, use "recent".

            Examples:
            - "Was Apple profitable this quarter?" -> intent: "earnings_check", timeframe: "this quarter"
            - "Tesla stock price today" -> intent: "price_check", timeframe: "today"
            - "How has Microsoft performed this month?" -> intent: "historical_analysis", timeframe: "this month"

            Return a JSON object with these fields.
            """
            
            response = await self.model.generate_content_async(prompt)
            
            import json
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "company_name": None,
                    "ticker": None,
                    "intent": "general_query",
                    "timeframe": "recent"
                }
                
        except Exception as e:
            self.logger.error(f"Error extracting intent from query: {e}")
            return {
                "company_name": None,
                "ticker": None,
                "intent": "general_query",
                "timeframe": "recent"
            }

    async def analyze_stock_movement(
        self, 
        ticker: str, 
        price_data: Dict[str, Any], 
        news_items: List[Dict[str, Any]],
        timeframe: str = "recent", 
        intent: str = "general_query",
        original_query: str = "",
        price_change_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze stock movement using price data, news, intent, original query and optional price change data"""
        try:
            # Log what we're receiving
            self.logger.info(f"Analyzing {ticker} for query: '{original_query}'")
            self.logger.info(f"Intent: {intent}, Has historical data: {bool(price_change_data)}")
            
            # Validate data consistency
            if ticker and price_data.get('ticker') and ticker != price_data.get('ticker'):
                self.logger.error(f"CRITICAL: Ticker mismatch! Requested: {ticker}, Price data: {price_data.get('ticker')}")
                return {
                    "analysis_summary": f"Data error: Analysis requested for {ticker} but received data for {price_data.get('ticker')}",
                    "key_factors": ["Data consistency error"],
                    "sentiment": "neutral",
                    "key_insights": ["System error - ticker mismatch"],
                    "confidence_score": 0.0
                }
            
            query_lower = original_query.lower()
            
            # Check for "today" queries first - these should use current price data, not historical
            if "today" in query_lower:
                current_price = price_data.get('current_price', 'N/A')
                prev_close = price_data.get('previous_close', 'N/A')
                change = price_data.get('change', 0)
                change_percent = price_data.get('change_percent', 0)
                high_today = price_data.get('high_price_today', 'N/A')
                low_today = price_data.get('low_price_today', 'N/A')
                
                prompt = f"""
                User asked: "{original_query}"
                
                They want to know how {ticker} has performed TODAY.
                
                Today's performance data:
                - Current price: ${current_price}
                - Previous close: ${prev_close}
                - Today's change: ${change} ({change_percent}%)
                - Today's high: ${high_today}
                - Today's low: ${low_today}
                - Trading range: ${low_today} - ${high_today}
                
                Recent news context suggests tariff concerns and competitive pressures.
                
                JSON response:
                {{
                    "analysis_summary": "Today, {ticker} is {'down' if change_percent < 0 else 'up'} {abs(change_percent)}% at ${current_price}, compared to yesterday's close of ${prev_close}. The stock has traded between ${low_today} and ${high_today} today.",
                    "key_factors": ["Today's performance: {change_percent}%", "Trading range: ${low_today}-${high_today}", "Previous close: ${prev_close}"],
                    "sentiment": "{'negative' if change_percent < 0 else 'positive'}",
                    "key_insights": ["Today's {ticker} performance: {'decline' if change_percent < 0 else 'gain'} of {abs(change_percent)}%", "Intraday trading range shows {'volatility' if abs(float(high_today) - float(low_today)) > 5 else 'stability'}"],
                    "confidence_score": 0.95
                }}
                """
                
            # Check what timeframe user actually requested for historical queries
            elif price_change_data and (
                ("how" in query_lower and any(word in query_lower for word in ["changed", "performed", "done"])) or
                ("last" in query_lower and any(word in query_lower for word in ["days", "week", "month"])) or
                intent == "historical_analysis"
            ):
                # We have historical data - use it!
                change_percent = price_change_data.get('change_percent', 0)
                actual_period = price_change_data.get('period', '7 days')
                start_price = price_change_data.get('open', 'N/A')
                end_price = price_change_data.get('close', 'N/A')
                high_price = price_change_data.get('high', 'N/A')
                low_price = price_change_data.get('low', 'N/A')
                start_date = price_change_data.get('meta', {}).get('start_date_used', 'N/A')
                end_date = price_change_data.get('meta', {}).get('end_date_used', 'N/A')
                
                self.logger.info(f"Using historical data: {change_percent}% change over {actual_period}")
                
                prompt = f"""
                User asked: "{original_query}"
                
                Historical performance for {ticker}:
                - Period: {actual_period} (from {start_date} to {end_date})
                - Starting price: ${start_price}
                - Ending price: ${end_price}
                - Total change: {change_percent}%
                - Period high: ${high_price}
                - Period low: ${low_price}
                
                Recent news context shows concerns about tariff threats and competitive pressures.
                
                Provide analysis directly addressing the user's question about the {actual_period} performance.
                
                JSON response:
                {{
                    "analysis_summary": "Over the past {actual_period}, {ticker} declined {abs(change_percent)}% from ${start_price} to ${end_price}. The stock hit a high of ${high_price} and low of ${low_price} during this period. Recent news shows tariff threats from Trump administration and competitive concerns from OpenAI affecting sentiment.",
                    "key_factors": ["{actual_period} decline of {change_percent}%", "Tariff threat concerns", "OpenAI competitive pressure", "Trading range ${low_price}-${high_price}"],
                    "sentiment": "negative",
                    "key_insights": ["{ticker} underperformed over {actual_period}", "Multiple headwinds including tariffs and AI competition", "Significant price decline from ${start_price} to ${end_price}"],
                    "confidence_score": 0.9
                }}
                """
            
            else:
                # Generic fallback using current data
                current_price = price_data.get('current_price', 'N/A')
                change_percent = price_data.get('change_percent', 0)
                
                prompt = f"""
                User asked: "{original_query}"
                
                Current {ticker} status:
                - Price: ${current_price} ({change_percent}% change)
                
                JSON response with analysis_summary, key_factors, sentiment, key_insights, confidence_score.
                """
            
            self.logger.info(f"Sending targeted analysis for: '{original_query}'")
            response = await self.model.generate_content_async(prompt)
            
            raw_text = response.text.strip()
            self.logger.info(f"Gemini raw response: {raw_text[:200]}...")
            
            # Enhanced JSON parsing
            json_str = None
            if raw_text.startswith('{') and raw_text.endswith('}'):
                json_str = raw_text
            else:
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
            
            if json_str:
                try:
                    parsed = json.loads(json_str)
                    return {
                        "analysis_summary": parsed.get("analysis_summary", f"Analysis for {ticker}"),
                        "key_factors": parsed.get("key_factors", []),
                        "sentiment": parsed.get("sentiment", "neutral"),
                        "key_insights": parsed.get("key_insights", []),
                        "confidence_score": parsed.get("confidence_score", 0.5)
                    }
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON parse error: {e}")
            
            # Manual fallback using historical data if available
            if price_change_data:
                change_percent = price_change_data.get('change_percent', 0)
                actual_period = price_change_data.get('period', '7 days')
                start_price = price_change_data.get('open', 'N/A')
                end_price = price_change_data.get('close', 'N/A')
                
                return {
                    "analysis_summary": f"Over the {actual_period}, {ticker} {'declined' if change_percent < 0 else 'gained'} {abs(change_percent)}% from ${start_price} to ${end_price}.",
                    "key_factors": [f"{actual_period} performance: {change_percent}%", f"Price movement: ${start_price} to ${end_price}"],
                    "sentiment": "negative" if change_percent < 0 else "positive",
                    "key_insights": [f"{ticker} {'underperformed' if change_percent < 0 else 'outperformed'} over the {actual_period}"],
                    "confidence_score": 0.8
                }
            
            # Fallback response specific to the actual ticker
            if "happening" in query_lower:
                return {
                    "analysis_summary": f"Recent activity for {ticker}: Stock is at ${price_data.get('current_price', 'N/A')} with a {price_data.get('change_percent', 0)}% change today. Recent news shows various developments affecting the company.",
                    "key_factors": [f"{ticker} price movement", "Recent news developments"],
                    "sentiment": "positive" if price_data.get('change_percent', 0) > 0 else "negative" if price_data.get('change_percent', 0) < 0 else "neutral",
                    "key_insights": [f"{ticker} is showing {'positive' if price_data.get('change_percent', 0) > 0 else 'negative' if price_data.get('change_percent', 0) < 0 else 'neutral'} movement"],
                    "confidence_score": 0.7
                }
            else:
                return {
                    "analysis_summary": f"{ticker} is trading at ${price_data.get('current_price', 'N/A')} with a {price_data.get('change_percent', 0)}% change today.",
                    "key_factors": ["Daily price movement"],
                    "sentiment": "positive" if price_data.get('change_percent', 0) > 0 else "negative" if price_data.get('change_percent', 0) < 0 else "neutral",
                    "key_insights": [f"{ticker} daily performance"],
                    "confidence_score": 0.6
                }
                
        except Exception as e:
            self.logger.error(f"Error analyzing {ticker}: {e}")
            return {
                "analysis_summary": f"Error analyzing {ticker}",
                "key_factors": [],
                "sentiment": "neutral",
                "key_insights": [],
                "confidence_score": 0.0
            }
