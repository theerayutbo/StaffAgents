from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from staffagents.agents.utils.agent_utils import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
    get_insider_sentiment,
    get_insider_transactions,
)
from staffagents.dataflows.config import get_config


def create_fundamentals_analyst(llm):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_fundamentals,
            get_balance_sheet,
            get_cashflow,
            get_income_statement,
        ]

        system_message = (
            "You are the Operational Analyst for the StaffAgents collective. Your mission is to audit the organisation's internal health over the past week—covering resource allocation, delivery performance, staffing considerations, and any financial or operational indicators that reveal execution readiness. Provide a deeply detailed narrative that executives can act on immediately, calling out strengths, bottlenecks, capacity gaps, and emerging opportunities."
            + " Close with a Markdown table that organises your key observations so they are simple to reference."
            + " Default to high-quality reasoning, Google sourced intelligence, and your model knowledge for context. Only reach for Alpha Vantage powered finance tools when the question explicitly involves financial performance that requires those datasets."
            + " You may use the available tools: `get_fundamentals` for comprehensive organisational fundamentals, `get_balance_sheet`, `get_cashflow`, and `get_income_statement` for specific financial statements when a finance deep dive is required."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS** or final deliverable,"
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
            "fundamentals_report": report,
        }

    return fundamentals_analyst_node
