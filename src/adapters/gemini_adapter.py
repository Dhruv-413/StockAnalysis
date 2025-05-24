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
            # Common company mappings
            common_companies = {
                "apple": {"company_name": "Apple Inc.", "ticker": "AAPL"},
                "microsoft": {"company_name": "Microsoft Corporation", "ticker": "MSFT"},
                "google": {"company_name": "Alphabet Inc.", "ticker": "GOOGL"},
                "alphabet": {"company_name": "Alphabet Inc.", "ticker": "GOOGL"},
                "amazon": {"company_name": "Amazon.com Inc.", "ticker": "AMZN"},
                "tesla": {"company_name": "Tesla Inc.", "ticker": "TSLA"},
                "nvidia": {"company_name": "NVIDIA Corporation", "ticker": "NVDA"},
                "meta": {"company_name": "Meta Platforms Inc.", "ticker": "META"},
                "facebook": {"company_name": "Meta Platforms Inc.", "ticker": "META"},
            }
            
            query_lower = query.lower()
            for name, details in common_companies.items():
                if name in query_lower:
                    prompt = f"""
                    Query: "{query}"
                    Company: "{details['company_name']}" (ticker: {details['ticker']})

                    Extract:
                    1. intent: "historical_analysis", "price_check", "news_summary", or "general_query"
                    2. timeframe: Time period mentioned (e.g., "7 days", "today", "last month")

                    Return JSON: {{"intent": "", "timeframe": ""}}
                    """
                    
                    response = await self.model.generate_content_async(prompt)
                    
                    try:
                        raw_text = response.text.strip()
                        
                        # Extract JSON from markdown
                        if "```json" in raw_text:
                            json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
                            if json_match:
                                raw_text = json_match.group(1)
                        
                        parsed_response = json.loads(raw_text)
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": parsed_response.get("intent", "general_query"),
                            "timeframe": parsed_response.get("timeframe", "recent")
                        }
                    except Exception:
                        # Fallback extraction
                        timeframe = "recent"
                        if "today" in query_lower:
                            timeframe = "today"
                        elif "30 days" in query_lower:
                            timeframe = "30 days"
                        elif "7 days" in query_lower:
                            timeframe = "7 days"
                        
                        return {
                            "company_name": details["company_name"],
                            "ticker": details["ticker"],
                            "intent": "general_query",
                            "timeframe": timeframe
                        }

            # General extraction for other companies
            prompt = f"""
            Analyze query: "{query}"

            Extract:
            1. "company_name": Full company name or null
            2. "ticker": Stock ticker symbol or null
            3. "intent": "earnings_check", "price_check", "historical_analysis", "news_summary", "company_profile", or "general_query"
            4. "timeframe": Time period mentioned or "recent"

            Return JSON object.
            """
            
            response = await self.model.generate_content_async(prompt)
            
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
            self.logger.error(f"Error extracting intent: {e}")
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
        """Analyze stock movement using AI"""
        try:
            # Validate ticker consistency
            if ticker and price_data.get('ticker') and ticker != price_data.get('ticker'):
                return {
                    "analysis_summary": f"Data error: Analysis requested for {ticker} but received data for {price_data.get('ticker')}",
                    "key_factors": ["Data consistency error"],
                    "sentiment": "neutral",
                    "key_insights": ["System error - ticker mismatch"],
                    "confidence_score": 0.0
                }
            
            query_lower = original_query.lower()
            
            # Build appropriate prompt based on query type
            if "today" in query_lower:
                current_price = price_data.get('current_price', 'N/A')
                change_percent = price_data.get('change_percent', 0)
                high_today = price_data.get('high_price_today', 'N/A')
                low_today = price_data.get('low_price_today', 'N/A')
                
                prompt = f"""
                Query: "{original_query}"
                
                Today's {ticker} performance:
                - Current: ${current_price}
                - Change: {change_percent}%
                - Range: ${low_today} - ${high_today}
                
                Return JSON with analysis_summary, key_factors, sentiment, key_insights, confidence_score.
                """
                
            elif price_change_data and (
                ("how" in query_lower and any(word in query_lower for word in ["changed", "performed"])) or
                ("last" in query_lower and any(word in query_lower for word in ["days", "week", "month"])) or
                intent == "historical_analysis"
            ):
                change_percent = price_change_data.get('change_percent', 0)
                period = price_change_data.get('period', '7 days')
                start_price = price_change_data.get('open', 'N/A')
                end_price = price_change_data.get('close', 'N/A')
                
                prompt = f"""
                Query: "{original_query}"
                
                {ticker} {period} performance:
                - Start: ${start_price}
                - End: ${end_price}
                - Change: {change_percent}%
                
                Return JSON with analysis_summary, key_factors, sentiment, key_insights, confidence_score.
                """
            
            else:
                current_price = price_data.get('current_price', 'N/A')
                change_percent = price_data.get('change_percent', 0)
                
                prompt = f"""
                Query: "{original_query}"
                
                {ticker} status:
                - Price: ${current_price} ({change_percent}% change)
                
                Return JSON with analysis_summary, key_factors, sentiment, key_insights, confidence_score.
                """
            
            response = await self.model.generate_content_async(prompt)
            raw_text = response.text.strip()
            
            # Parse JSON response
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
                    
                    # Ensure confidence_score is a number
                    confidence_score = parsed.get("confidence_score", 0.7)
                    if isinstance(confidence_score, str):
                        try:
                            if "/" in confidence_score:
                                parts = confidence_score.split("/")
                                confidence_score = float(parts[0]) / float(parts[1])
                            else:
                                confidence_score = float(confidence_score)
                        except:
                            confidence_score = 0.7
                    
                    if confidence_score > 1:
                        confidence_score = confidence_score / 100
                    
                    return {
                        "analysis_summary": parsed.get("analysis_summary", f"Analysis for {ticker}"),
                        "key_factors": parsed.get("key_factors", []),
                        "sentiment": parsed.get("sentiment", "neutral"),
                        "key_insights": parsed.get("key_insights", []),
                        "confidence_score": confidence_score
                    }
                except json.JSONDecodeError:
                    pass
            
            # Fallback response
            if price_change_data:
                change_percent = price_change_data.get('change_percent', 0)
                period = price_change_data.get('period', '7 days')
                
                return {
                    "analysis_summary": f"Over {period}, {ticker} {'declined' if change_percent < 0 else 'gained'} {abs(change_percent)}%.",
                    "key_factors": [f"{period} performance: {change_percent}%"],
                    "sentiment": "negative" if change_percent < 0 else "positive",
                    "key_insights": [f"{ticker} {'underperformed' if change_percent < 0 else 'outperformed'} over {period}"],
                    "confidence_score": 0.8
                }
            
            return {
                "analysis_summary": f"{ticker} is trading at ${price_data.get('current_price', 'N/A')} with a {price_data.get('change_percent', 0)}% change.",
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
