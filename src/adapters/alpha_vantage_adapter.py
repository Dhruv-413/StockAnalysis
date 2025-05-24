import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, List, Any

from .base_adapter import BaseAdapter 
from src.config import settings
from ..utils.cache import cached # Corrected import for cache

class AlphaVantageAdapter(BaseAdapter):
    """
    Adapter for fetching stock data from Alpha Vantage API.
    """
    def __init__(self):
        api_key = settings.alpha_vantage_api_key
        if not api_key:
            self.logger.warning("Alpha Vantage API key is not configured. Adapter functionality will be limited.")
        
        super().__init__(
            api_key=api_key or "DUMMY_KEY_IF_NONE",
            base_url=settings.alpha_vantage_base_url
        )
        if not api_key:
            self.api_key = None

    def _get_auth_params(self) -> Dict[str, str]:
        return {}

    @cached(ttl=3600)
    async def get_global_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get current quote using GLOBAL_QUOTE endpoint"""
        if not self.api_key:
            self.logger.error(f"Alpha Vantage API key not available for quote {ticker}")
            return None
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            data = response.json()
            
            quote = data.get("Global Quote", {})
            if not quote:
                self.logger.warning(f"No quote data for {ticker}: {data}")
                return None
            
            return {
                "current_price": float(quote.get("05. price", 0)),
                "previous_close": float(quote.get("08. previous close", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": float(quote.get("10. change percent", "0%").rstrip('%')),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "open": float(quote.get("02. open", 0)),
                "volume": int(quote.get("06. volume", 0))
            }
        except Exception as e:
            self.logger.error(f"Error getting quote for {ticker}: {e}")
            return None

    @cached(ttl=3600)
    async def get_daily_time_series(
        self, ticker: str, output_size: str = "compact"
    ) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Fetches daily time series using TIME_SERIES_DAILY (free tier).
        output_size: "compact" for last 100 data points, "full" for 20+ years.
        """
        if not self.api_key:
            self.logger.error(f"Alpha Vantage API key not available for daily series {ticker}")
            return None
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": output_size
        }
        
        self.logger.info(f"Requesting TIME_SERIES_DAILY for {ticker} with outputsize={output_size}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" not in data:
                self.logger.warning(f"No daily time series for {ticker}: {data.get('Information', data.get('Error Message', 'Unknown error'))}")
                return None
            
            self.logger.info(f"Successfully fetched daily time series for {ticker}")
            return data["Time Series (Daily)"]
            
        except Exception as e:
            self.logger.error(f"Error getting daily time series for {ticker}: {e}")
            return None

    @cached(ttl=7200) # Cache weekly data for 2 hours
    async def get_weekly_time_series(self, ticker: str) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Fetches weekly time series using TIME_SERIES_WEEKLY (free tier).
        Covers 20+ years of historical data.
        """
        if not self.api_key:
            self.logger.error(f"Alpha Vantage API key not available for weekly series {ticker}")
            return None
        
        params = {
            "function": "TIME_SERIES_WEEKLY",
            "symbol": ticker,
            "apikey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            data = response.json()

            if "Weekly Time Series" not in data:
                self.logger.warning(f"No weekly time series for {ticker}: {data.get('Information', data.get('Error Message', 'Unknown error'))}")
                return None
            
            return data["Weekly Time Series"]
            
        except Exception as e:
            self.logger.error(f"Error getting weekly time series for {ticker}: {e}")
            return None

    @cached(ttl=14400) # Cache monthly data for 4 hours
    async def get_monthly_time_series(self, ticker: str) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Fetches monthly time series using TIME_SERIES_MONTHLY (free tier).
        Covers 20+ years of historical data.
        """
        if not self.api_key:
            self.logger.error(f"Alpha Vantage API key not available for monthly series {ticker}")
            return None
        
        params = {
            "function": "TIME_SERIES_MONTHLY",
            "symbol": ticker,
            "apikey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            data = response.json()

            if "Monthly Time Series" not in data:
                self.logger.warning(f"No monthly time series for {ticker}: {data.get('Information', data.get('Error Message', 'Unknown error'))}")
                return None
            
            return data["Monthly Time Series"]
            
        except Exception as e:
            self.logger.error(f"Error getting monthly time series for {ticker}: {e}")
            return None

    async def get_historical_data_optimized(
        self, ticker: str, days_ago: int
    ) -> Optional[Dict[str, Any]]:
        """
        Enhanced method to get historical data based on timeframe.
        Uses appropriate endpoint (daily/weekly/monthly) based on duration.
        """
        self.logger.info(f"Getting optimized historical data for {ticker} over {days_ago} days")
        
        if days_ago <= 0:
            return None

        try:
            # Choose appropriate endpoint based on timeframe - use full data for 30+ days
            if days_ago <= 30:  # Up to 30 days - use daily compact or full
                if days_ago <= 7:
                    time_series = await self.get_daily_time_series(ticker, "compact")
                else:
                    time_series = await self.get_daily_time_series(ticker, "full")  # Use full for longer periods
                series_key = "4. close"
                high_key = "2. high"
                low_key = "3. low"
            elif days_ago <= 365:  # Less than 1 year - use daily full
                time_series = await self.get_daily_time_series(ticker, "full")
                series_key = "4. close"
                high_key = "2. high"
                low_key = "3. low"
            elif days_ago <= 365 * 2:  # Less than 2 years - use weekly
                time_series = await self.get_weekly_time_series(ticker)
                series_key = "4. close"
                high_key = "2. high"
                low_key = "3. low"
                days_ago = days_ago // 7  # Convert to weeks
            else:  # More than 2 years - use monthly
                time_series = await self.get_monthly_time_series(ticker)
                series_key = "4. close"
                high_key = "2. high"
                low_key = "3. low"
                days_ago = days_ago // 30  # Convert to months

            if not time_series:
                self.logger.warning(f"No time series data for {ticker}")
                return None

            sorted_dates = sorted(time_series.keys(), reverse=True)
            if not sorted_dates or len(sorted_dates) < 2:
                self.logger.warning(f"Insufficient data points for {ticker}")
                return None

            # Get most recent price (end price)
            recent_date_str = sorted_dates[0]
            recent_price_str = time_series[recent_date_str].get(series_key)
            recent_price = float(recent_price_str) if recent_price_str else None

            if recent_price is None:
                self.logger.warning(f"No recent price data for {ticker}")
                return None

            # Find historical price exactly days_ago back
            target_past_date_dt = datetime.now() - timedelta(days=days_ago)
            
            closest_past_date_str = None
            min_diff_days = float('inf')

            # Find the closest past date to our target
            for date_str in sorted_dates:
                try:
                    data_date_dt = datetime.strptime(date_str, "%Y-%m-%d")
                    if data_date_dt <= target_past_date_dt:
                        diff = abs((target_past_date_dt - data_date_dt).days)
                        if diff < min_diff_days:
                            min_diff_days = diff
                            closest_past_date_str = date_str
                        if diff <= 3:  # Good enough match (within 3 days)
                            break
                except ValueError:
                    continue
            
            # If no good past date found, use the oldest available
            if not closest_past_date_str and len(sorted_dates) > days_ago // 7:
                # Try to get approximately the right timeframe
                target_index = min(days_ago, len(sorted_dates) - 1)
                closest_past_date_str = sorted_dates[target_index]

            if not closest_past_date_str:
                self.logger.warning(f"Could not find suitable past date for {ticker}")
                return None
                
            past_price_str = time_series[closest_past_date_str].get(series_key)
            past_price = float(past_price_str) if past_price_str else None

            if past_price is None:
                self.logger.warning(f"No past price data for {ticker}")
                return None

            # Calculate change
            price_change = recent_price - past_price
            price_change_percent = (price_change / past_price) * 100 if past_price != 0 else 0

            # Get period high and low from the data range
            period_highs = []
            period_lows = []
            
            # Find the index range for our period
            start_idx = sorted_dates.index(closest_past_date_str)
            end_idx = sorted_dates.index(recent_date_str)
            
            for date_str in sorted_dates[end_idx:start_idx + 1]:
                high_str = time_series[date_str].get(high_key)
                low_str = time_series[date_str].get(low_key)
                
                if high_str:
                    try:
                        period_highs.append(float(high_str))
                    except ValueError:
                        pass
                if low_str:
                    try:
                        period_lows.append(float(low_str))
                    except ValueError:
                        pass
            
            period_high = max(period_highs) if period_highs else recent_price
            period_low = min(period_lows) if period_lows else recent_price

            result = {
                "period_description": f"{days_ago} days",
                "start_date": closest_past_date_str,
                "end_date": recent_date_str,
                "start_price": round(past_price, 2),
                "end_price": round(recent_price, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "period_high": round(period_high, 2),
                "period_low": round(period_low, 2),
                "data_points": abs(start_idx - end_idx) + 1
            }

            self.logger.info(f"Successfully calculated historical data for {ticker} over {days_ago} days: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error in get_historical_data_optimized for {ticker}: {e}")
            return None

    async def get_price_change_over_period(
        self, ticker: str, days_ago: int
    ) -> Optional[Dict[str, Any]]:
        """
        Enhanced method that uses optimized historical data fetching.
        """
        return await self.get_historical_data_optimized(ticker, days_ago)

    @cached(ttl=1800)
    async def get_intraday_data(
        self, ticker: str, interval: str = "60min", output_size: str = "compact"
    ) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Get intraday data using TIME_SERIES_INTRADAY (free tier).
        interval: 1min, 5min, 15min, 30min, 60min
        output_size: compact (100 data points) or full (30 days)
        """
        if not self.api_key:
            self.logger.error(f"Alpha Vantage API key not available for intraday data {ticker}")
            return None
        
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": ticker,
            "interval": interval,
            "outputsize": output_size,
            "apikey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            data = response.json()

            series_key = f"Time Series ({interval})"
            if series_key not in data:
                self.logger.warning(f"No intraday data for {ticker}: {data.get('Information', data.get('Error Message', 'Unknown error'))}")
                return None
            
            return data[series_key]
            
        except Exception as e:
            self.logger.error(f"Error getting intraday data for {ticker}: {e}")
            return None

    async def get_comprehensive_analysis_data(
        self, ticker: str, days_ago: int
    ) -> Dict[str, Any]:
        """
        Get comprehensive data for analysis including multiple timeframes.
        """
        self.logger.info(f"Getting comprehensive analysis data for {ticker} over {days_ago} days")
        
        # Get current quote
        current_quote = await self.get_global_quote(ticker)
        
        # Get historical price change
        price_change = await self.get_historical_data_optimized(ticker, days_ago)
        
        # Get additional context data based on timeframe
        additional_data = {}
        
        if days_ago <= 7:  # Short term - get intraday data
            intraday = await self.get_intraday_data(ticker, "60min", "full")
            if intraday:
                additional_data["intraday_pattern"] = "available"
        elif days_ago <= 365:  # Medium term - get weekly context
            weekly = await self.get_weekly_time_series(ticker)
            if weekly:
                additional_data["weekly_trend"] = "available"
        else:  # Long term - get monthly context
            monthly = await self.get_monthly_time_series(ticker)
            if monthly:
                additional_data["monthly_trend"] = "available"
        
        return {
            "current_quote": current_quote,
            "price_change": price_change,
            "additional_context": additional_data,
            "analysis_timeframe": days_ago
        }

