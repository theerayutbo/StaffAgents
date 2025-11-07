from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Use a different model
config["quick_think_llm"] = "gpt-4o-mini"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds

'''
# ...existing code...
# Create a custom config
config = DEFAULT_CONFIG.copy()
# Use Gemini models and Google as provider
config["llm_provider"] = "google"                 # provider used by your LLM wrapper
config["deep_think_llm"] = "gemini-1.5-pro"       # example: gemini-1.5-pro, gemini-1.0, gemini-mini
config["quick_think_llm"] = "gemini-mini"         # smaller Gemini for quick tasks
config["max_debate_rounds"] = 1  # Increase debate rounds
# ...existing code...
'''

# Configure data vendors (default uses yfinance and alpha_vantage)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: yfinance, alpha_vantage, local
    "technical_indicators": "yfinance",      # Options: yfinance, alpha_vantage, local
    "fundamental_data": "alpha_vantage",     # Options: openai, alpha_vantage, local
    "news_data": "alpha_vantage",            # Options: openai, alpha_vantage, google, local
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2025-11-04")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
