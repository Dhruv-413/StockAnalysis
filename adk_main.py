from adk_agents.main import stock_analysis_agent
from adk_agents.agent import root_agent 

# This module exports the main agent to be used with 'adk api_server'
# Main agent is now registered with ADK and will be discoverable

if __name__ == "__main__":
    print("\n✅ Stock Analysis Agent successfully registered with ADK")
    print("\nIMPORTANT: For ADK to discover your agent, you must run the server from the root directory")
    print("  where the agent.py file is located.")
    print("\nTo start the ADK server, run:")
    print("   adk api_server --allow_origins=http://localhost:4200 --host=0.0.0.0")
    print("\nTo connect with ADK Web, run (in the adk-web directory):")  
    print("   npm run serve --backend=http://localhost:8000")
    print("\nThen visit http://localhost:4200 in your browser")
    print("\nAvailable agents:")
    print("   - StockAnalysisAgent: Main analysis workflow")
    print("\nExample query: \"How is Apple stock doing today?\"")
