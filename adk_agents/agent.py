"""
Root agent entry point for Google ADK.
This file must be at the root level for ADK to discover it.
"""
from typing import ClassVar
from google.adk.agents import LlmAgent

class StockAnalysisAgent(LlmAgent):
    root_agent: ClassVar[bool] = True
    
    def __init__(self):
        super().__init__(name="StockAnalysisAgent", model="gemini-1.5-flash")  # Specify model
    
    async def run(self, query: str) -> str:
        """Main method that ADK will call"""
        # Use your existing orchestrator logic
        from src.orchestrator.main_orchestrator import MainOrchestrator
        from src.models.schemas import AnalysisRequest
        
        orchestrator = MainOrchestrator()
        request = AnalysisRequest(query=query)
        result = await orchestrator.process_request(request)
        
        return f"""
        **{result.ticker} Analysis**
        
        {result.analysis_summary}
        
        **Price**: ${result.price_data.current_price if result.price_data else 'N/A'}
        **Change**: {result.price_data.change_percent if result.price_data else 'N/A'}%
        **Sentiment**: {result.sentiment or 'neutral'}
        
        **Key Insights:**
        {chr(10).join(f"• {insight}" for insight in result.key_insights)}
        """

# Create the agent instance that ADK expects
agent = StockAnalysisAgent()
root_agent = agent
