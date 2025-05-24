from typing import Dict, Any
from .base_agent import BaseAgent
from src.adapters.finnhub_adapter import FinnhubAdapter
from src.adapters.gemini_adapter import GeminiAdapter

class TickerIdentificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("TickerIdentificationAgent")
        self.finnhub = FinnhubAdapter()
        self.gemini = GeminiAdapter()
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify ticker from query or company name"""
        query = input_data.get("query", "")
        # These are from Gemini's intent extraction
        extracted_company_name = input_data.get("company_name")
        extracted_ticker = input_data.get("ticker")
        
        # Priority 1: If Gemini provided a ticker and a company name
        if extracted_ticker and extracted_company_name:
            # Validate the extracted_ticker with Finnhub
            profile = await self.finnhub.get_company_profile(extracted_ticker)
            if profile and profile.get("name"):
                if extracted_company_name.lower() in profile.get("name", "").lower() or \
                   profile.get("name", "").lower() in extracted_company_name.lower():
                    self.logger.info(f"Validated ticker {extracted_ticker} for company {profile.get('name')} from Gemini's extraction.")
                    return {
                        "ticker": extracted_ticker.upper(),
                        "company_name": profile["name"],
                        "profile_data": profile,
                        "confidence": 0.95
                    }
                else:
                    self.logger.warning(f"Gemini's ticker {extracted_ticker} (Finnhub name: {profile.get('name')}) "
                                        f"does not strongly match Gemini's company name {extracted_company_name}. Will try searching by company name.")
            # If ticker validation failed or names didn't match well, proceed to search by company_name

        # Priority 2: If Gemini provided a company name
        if extracted_company_name:
            self.logger.info(f"Attempting to find ticker for company name: {extracted_company_name}")
            ticker_from_search = await self.finnhub.search_ticker(extracted_company_name)
            if ticker_from_search:
                profile = await self.finnhub.get_company_profile(ticker_from_search)
                if profile and profile.get("name"):
                    self.logger.info(f"Found ticker {ticker_from_search} for company {profile.get('name')} via Finnhub search.")
                    return {
                        "ticker": ticker_from_search.upper(),
                        "company_name": profile["name"],
                        "profile_data": profile,
                        "confidence": 0.9
                    }
                elif profile: # Profile exists but no name
                     return {
                        "ticker": ticker_from_search.upper(),
                        "company_name": extracted_company_name,
                        "profile_data": profile,
                        "confidence": 0.85
                    }


        # Priority 3: If Gemini only provided a ticker
        if extracted_ticker and not extracted_company_name:
            self.logger.info(f"Attempting to validate ticker provided by Gemini (without company name context): {extracted_ticker}")
            profile = await self.finnhub.get_company_profile(extracted_ticker)
            if profile and profile.get("name"):
                return {
                    "ticker": extracted_ticker.upper(),
                    "company_name": profile["name"],
                    "profile_data": profile,
                    "confidence": 0.8
                }
        
        # Fallback: Original logic of trying words from the query
        if query:
            self.logger.info(f"Falling back to query word search for: {query}")
            stop_words = {"why", "did", "stock", "drop", "today", "what", "how", "has", "changed", "the", "last", "days", "recently", "happening", "with", "me", "about", "history", "tell"}
            
            query_words = [word.strip("?.,!").lower() for word in query.split()]
            potential_company_phrases = []
            for i in range(len(query_words)):
                if query_words[i] not in stop_words:
                    potential_company_phrases.append(query_words[i].title())
                    if i + 1 < len(query_words) and query_words[i+1] not in stop_words:
                        potential_company_phrases.append(f"{query_words[i].title()} {query_words[i+1].title()}") # Two words
            
            for phrase in sorted(potential_company_phrases, key=len, reverse=True):
                if len(phrase) < 3 and not phrase.isupper(): continue 
                try:
                    ticker_from_phrase_search = await self.finnhub.search_ticker(phrase)
                    if ticker_from_phrase_search:
                        profile = await self.finnhub.get_company_profile(ticker_from_phrase_search)
                        if profile and profile.get("name"):
                            return {
                                "ticker": ticker_from_phrase_search.upper(),
                                "company_name": profile.get("name", phrase) if profile else phrase,
                                "profile_data": profile if profile else {},
                                "confidence": 0.7 if len(phrase.split()) > 1 else 0.6 
                            }
                except Exception as e:
                    self.logger.warning(f"Finnhub search failed for fallback phrase '{phrase}': {e}")
                    continue
        
        # No ticker found
        self.logger.error(f"Could not identify ticker or company from input: query='{query}', extracted_company='{extracted_company_name}', extracted_ticker='{extracted_ticker}'")
        return {
            "ticker": None,
            "company_name": None,
            "profile_data": None,
            "confidence": 0.0,
            "error": "Could not identify ticker or company from input"
        }
