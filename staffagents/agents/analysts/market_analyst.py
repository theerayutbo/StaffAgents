from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from staffagents.agents.utils.agent_utils import get_stock_data, get_indicators
from staffagents.dataflows.config import get_config


def create_market_analyst(llm):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_stock_data,
            get_indicators,
        ]

        system_message = (
            "You are the Strategic Analyst within StaffAgents. Synthesise the organisation's forward-looking position by selecting the most relevant performance signals from the toolkit below. Focus on insights that guide executive prioritisation—momentum, volatility, capacity for acceleration, and leading indicators that foreshadow inflection points."
            + " Choose at most eight complementary indicators across these categories so your briefing covers trend health, momentum, volatility, and volume-backed conviction."
            + " Moving Averages: close_10_ema, close_50_sma, close_200_sma for short-, mid-, and long-horizon direction."
            + " MACD Suite: macd, macds, macdh to unpack momentum shifts and turning points."
            + " Momentum Indicator: rsi for stress-testing extremes or fatigue."
            + " Volatility + Guardrails: boll, boll_ub, boll_lb, atr for understanding buffer, pressure, and variability."
            + " Volume Context: vwma to confirm whether momentum is supported by engagement."
            + " Always call `get_stock_data` first to gather the base signal, then request the specific indicators you need via `get_indicators` (use the exact names above). Default to Google and LLM-derived reasoning; invoke Alpha Vantage-backed metrics only when the leadership explicitly seeks financial market confirmation."
            + " Produce a richly detailed narrative of what these signals mean for strategic direction. Avoid vague statements—explain the implications for pacing, investment, and focus areas. Conclude with a Markdown table that captures each signal, the insight it provides, and recommended strategic moves."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS** or deliverable,"
                    " prefix your response with FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content
       
        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
