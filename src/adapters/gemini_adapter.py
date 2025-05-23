import google.generativeai as genai
from typing import Dict, Any, List, Optional
from src.config import settings
from src.utils.logger import setup_logger
from src.utils.cache import cached

class GeminiAdapter:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.logger = setup_logger(self.__class__.__name__)
    
    @cached(ttl=1800)  # Cache for 30 minutes
    async def analyze_stock_movement(
        self, 
        ticker: str, 
        price_data: Dict[str, Any], 
        news_items: List[Dict[str, Any]],
        timeframe: str = "recent"
    ) -> Dict[str, Any]:
        """Analyze stock movement using price data and news"""
        try:
            # Prepare context for analysis
            news_context = "\n".join([
                f"- {item['title']}: {item.get('summary', 'No summary')}"
                for item in news_items[:5]
            ])
            
            price_context = f"""
            Current Price: ${price_data.get('current_price', 'N/A')}
            Previous Close: ${price_data.get('previous_close', 'N/A')}
            Change: {price_data.get('change', 'N/A')} ({price_data.get('change_percent', 'N/A')}%)
            Volume: {price_data.get('volume', 'N/A')}
            """
            
            prompt = f"""
            Analyze the stock movement for {ticker} based on the following data:
            
            PRICE DATA:
            {price_context}
            
            RECENT NEWS:
            {news_context}
            
            Please provide:
            1. A concise analysis of why the stock moved
            2. Key factors influencing the price
            3. Sentiment (positive/negative/neutral)
            4. 3-5 key insights
            5. Confidence score (0-1) for your analysis
            
            Your response MUST be a raw JSON object. Do NOT wrap it in markdown (e.g. ```json ... ```).
            The JSON object should have the following structure:
            {{
                "analysis_summary": "Brief explanation of stock movement",
                "key_factors": ["factor1", "factor2", "factor3"],
                "sentiment": "positive/negative/neutral",
                "key_insights": ["insight1", "insight2", "insight3"],
                "confidence_score": 0.85
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            import json
            import re
            
            raw_text = response.text.strip()
            json_str_to_parse = None

            # Attempt to find JSON within markdown code blocks first
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL | re.IGNORECASE)
            if match:
                json_str_to_parse = match.group(1)
            elif raw_text.startswith('{') and raw_text.endswith('}'):
                # If not in markdown, check if the whole string is a JSON object
                json_str_to_parse = raw_text
            
            if json_str_to_parse:
                try:
                    parsed_json = json.loads(json_str_to_parse)
                    # Standardize the output structure
                    return {
                        "analysis_summary": parsed_json.get("analysis_summary", f"Analysis for {ticker} not fully available."),
                        "key_factors": parsed_json.get("key_factors", []),
                        "sentiment": parsed_json.get("sentiment", "neutral"),
                        "key_insights": parsed_json.get("key_insights", []),
                        "confidence_score": parsed_json.get("confidence_score", 0.5)
                    }
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSONDecodeError after attempting to extract/parse JSON for {ticker}: {e}. Raw text: {raw_text[:500]}")
            
            # Fallback if JSON parsing or extraction fails or no clear JSON structure found
            self.logger.warning(f"Could not parse valid JSON from Gemini for {ticker}. Using raw text as summary. Raw text: {raw_text[:500]}")
            return {
                "analysis_summary": raw_text if raw_text else f"Unable to analyze {ticker} at this time. AI response was empty or invalid.",
                "key_factors": [],
                "sentiment": "neutral",
                "key_insights": [f"AI response for {ticker} was not in the expected JSON format." if raw_text else "AI response was empty."],
                "confidence_score": 0.1 
            }
                
        except Exception as e:
            self.logger.error(f"Error analyzing stock {ticker}: {e}")
            return {
                "analysis_summary": f"Unable to analyze {ticker} at this time",
                "key_factors": [],
                "sentiment": "neutral",
                "key_insights": [],
                "confidence_score": 0.0
            }
    
    @cached(ttl=300)  # Cache for 5 minutes
    async def extract_intent_and_ticker(self, query: str) -> Dict[str, Any]:
        """Extract intent and ticker from natural language query"""
        try:
            # Simple pre-check for very common company names
            # This can be expanded or made more sophisticated
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
                "nike": {"company_name": "NIKE, Inc.", "ticker": "NKE"},  # Added Nike
            }
            
            query_lower = query.lower()
            for name, details in common_companies_map.items():
                if name in query_lower:
                    # If a common company name is found, prioritize it.
                    # We can still let Gemini try to parse intent and timeframe.
                    self.logger.info(f"Common company '{name}' found in query. Using predefined details and extracting rest with Gemini.")
                    
                    # Prompt Gemini for intent and timeframe, but provide the company context
                    prompt_for_common = f"""
                    Given the query: "{query}"
                    And knowing the primary company of interest is "{details['company_name']}" (ticker: {details['ticker']}).

                    Extract the following:
                    1. intent: What the user wants (e.g., price, news, analysis, history, general_info).
                    2. timeframe: Time period mentioned (e.g., today, week, month, 7 days, specific year).

                    Return a JSON response with "intent" and "timeframe".
                    Example response:
                    {{
                        "intent": "stock_history",
                        "timeframe": "overall"
                    }}
                    """
                    response_common = await self.model.generate_content_async(prompt_for_common)
                    import json
                    try:
                        parsed_common_response = json.loads(response_common.text)
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": parsed_common_response.get("intent", "general_query"),
                            "timeframe": parsed_common_response.get("timeframe", "recent")
                        }
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to parse Gemini response for common company intent: {response_common.text}")
                        # Fallback to original details if intent/timeframe extraction fails
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": "general_query",
                            "timeframe": "recent"
                        }

            # If no common company name was pre-identified, proceed with the general Gemini extraction
            prompt = f"""
            Analyze the following stock-related query: "{query}"

            Identify the primary company or stock ticker the user is interested in.
            Also, determine the user's intent and any specified timeframe.

            Return a JSON object with the following fields:
            1. "company_name": The full official name of the company if identifiable (e.g., "Apple Inc.", "NVIDIA Corporation"). If a common term like "Apple" is used, provide the full name. If no specific company is clear, set to null.
            2. "ticker": The stock ticker symbol if explicitly mentioned or clearly implied by the company name (e.g., "AAPL" for Apple). If no ticker is clear, set to null.
            3. "intent": The user's primary goal (e.g., "price_check", "news_summary", "historical_performance", "company_analysis", "general_query").
            4. "timeframe": Any time period mentioned (e.g., "today", "last 7 days", "past year", "Q3 2023"). If not specified, use "recent".

            Prioritize well-known companies. For example, if the query is "tell me about apple stock", "company_name" should be "Apple Inc." and "ticker" should be "AAPL".
            Avoid interpreting common English words (like "tell", "show", "about") as company names or tickers unless they are part of a clear company name (e.g., "Tellurian Inc.").

            Example for "What's the news on Microsoft today?":
            {{
                "company_name": "Microsoft Corporation",
                "ticker": "MSFT",
                "intent": "news_summary",
                "timeframe": "today"
            }}

            Example for "NVDA stock price":
            {{
                "company_name": "NVIDIA Corporation", 
                "ticker": "NVDA",
                "intent": "price_check",
                "timeframe": "recent"
            }}
            
            Example for "Tell me about Ford":
            {{
                "company_name": "Ford Motor Company",
                "ticker": "F",
                "intent": "general_query",
                "timeframe": "recent"
            }}

            If the query is vague or doesn't mention a specific stock, like "How is the market doing?", set company_name and ticker to null.
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
                "intent": "error",
                "timeframe": "recent"
            }
