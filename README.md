````markdown
# StaffAgents: Multi-Agents LLM Organizational Intelligence Framework

> StaffAgents officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

🚀 [StaffAgents](#staffagents-framework) | ⚡ [Installation & CLI](#installation-and-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Package Usage](#staffagents-package) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

## StaffAgents Framework

StaffAgents is a multi-agent collaboration framework that mirrors the dynamics of real-world strategic planning teams. By deploying specialized LLM-powered analysts—from strategic planners and operational reviewers to marketing specialists and risk scouts—the platform collaboratively evaluates organizational context and surfaces coordinated recommendations. Moreover, these agents engage in dynamic discussions to pinpoint the optimal course of action for leadership.

> StaffAgents framework is designed for research purposes. Outcomes may vary based on the chosen backbone language models, model temperature, time horizons, the quality of data, and other non-deterministic factors. Adapt the framework to your internal review policies before using it in production environments.

Our framework decomposes complex organizational questions into specialized roles. This ensures the system achieves a robust, scalable approach to cross-functional analysis and decision-making.

### Analyst Team
- **Strategic Analyst**: Synthesizes performance indicators, competitive positioning, and long-term opportunities to guide enterprise strategy.
- **Operational Analyst**: Reviews fundamentals, resource allocation, and process efficiency to highlight execution improvements.
- **Marketing & Customer Analyst**: Aggregates sentiment, feedback, and market conversations to surface customer-centric insights.
- **Risk & External Analyst**: Tracks regulatory shifts, partner ecosystems, and macro trends to flag external risks and opportunities.

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

### Staff Coordinator Agent
- Composes reports from the analysts and researchers to craft unified action plans. It aligns stakeholders on next steps based on comprehensive organizational intelligence.

### Risk Management and Executive Review
- Continuously evaluates operational risk by assessing volatility in key metrics, stakeholder sentiment, and external dependencies. The risk management team refines proposed actions before they move forward.
- The Executive Review function approves or redirects the coordination plan. When approved, recommendations become ready for implementation.

## Installation and CLI

### Installation

Clone StaffAgents:
```bash
git clone [https://github.com/theerayutbo/StaffAgents.git](https://github.com/theerayutbo/StaffAgents.git)
cd StaffAgents
````

Create a virtual environment in any of your favorite environment managers:

```bash
conda create -n staffagents python=3.13
conda activate staffagents
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Required APIs

You will need the OpenAI API for all the agents. An [Alpha Vantage API](https://www.alphavantage.co/support/#api-key) key is optional—StaffAgents only reaches for Alpha Vantage when a prompt explicitly requests finance-specific data, otherwise it relies on Google and LLM-sourced intelligence by default.

```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
export ALPHA_VANTAGE_API_KEY=$YOUR_ALPHA_VANTAGE_API_KEY
```

Alternatively, you can create a `.env` file in the project root with your API keys (see `.env.example` for reference):

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

**Note:** We are happy to partner with Alpha Vantage to provide robust API support for StaffAgents. You can get a free AlphaVANTAGE API [here](https://www.alphavantage.co/support/#api-key); StaffAgents-sourced requests also have increased rate limits to 60 requests per minute with no daily limits. In this reimagined organisational workflow, Google and LLM-synthesised sources are the primary defaults, and Alpha Vantage is consulted only when a question clearly requires financial context. You can fine-tune this behaviour via the data vendor settings in `staffagents/default_config.py`.

### CLI Usage

You can also try out the CLI directly by running:

```bash
python -m cli.main
```

You will see a screen where you can select your desired tickers, date, LLMs, research depth, etc.

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

## StaffAgents Package

### Implementation Details

We built StaffAgents with LangGraph to ensure flexibility and modularity. We utilize `o1-preview` and `gpt-4o` as our deep thinking and fast thinking LLMs for our experiments. However, for testing purposes, we recommend you use `o4-mini` and `gpt-4.1-mini` to save on costs as our framework makes **lots of** API calls.

### Python Usage

To use StaffAgents inside your code, you can import the lightweight alias and initialize a `StaffAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from staffagents import StaffAgentsGraph
from staffagents.default_config import DEFAULT_CONFIG

ta = StaffAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("Customer Experience Initiative", "2025-11-04")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from staffagents import StaffAgentsGraph
from staffagents.default_config import DEFAULT_CONFIG

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds

# Configure data vendors (default uses yfinance with Google/LLM-first fundamentals & news)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",          # Options: yfinance, alpha_vantage, local
    "technical_indicators": "yfinance",      # Options: yfinance, alpha_vantage, local
    "fundamental_data": "openai,alpha_vantage",      # Options: openai, alpha_vantage, local
    "news_data": "google,openai,alpha_vantage",        # Options: openai, alpha_vantage, google, local
}

# Initialize with custom config
ta = StaffAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("Customer Experience Initiative", "2025-11-04")
print(decision)
```

> The default configuration uses yfinance for stock price and technical data, combines Google search with LLM synthesis for fundamental and news analysis, and falls back to Alpha Vantage only when finance-specific answers are requested. For production use or if you encounter rate limits, consider upgrading to [Alpha Vantage Premium](https://www.alphavantage.co/premium/) for more stable and reliable data access. For offline experimentation, there's a local data vendor option that uses our **Tauric TradingDB**, a curated dataset for backtesting, though this is still in development. We're currently refining this dataset and plan to release it soon alongside our upcoming projects. Stay tuned\!

You can view the full list of configurations in `staffagents/default_config.py`.

## Contributing

This project I get inspiration from the projecy of the open-source financial AI research community [Tauric Research](https://tauric.ai/).

## Citation

This project is inspired by and builds upon the framework presented in the original **tradingagents** paper. If you find the code in this repository helpful, please cite the original authors' work:

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
