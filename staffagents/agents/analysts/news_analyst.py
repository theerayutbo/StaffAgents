from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from staffagents.agents.utils.agent_utils import get_news, get_global_news
from staffagents.dataflows.config import get_config


def create_news_analyst(llm):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        tools = [
            get_news,
            get_global_news,
        ]

        system_message = (
            "You are the Risk & External Analyst for StaffAgents. Examine the past week of developments to chart regulatory updates, geopolitical moves, competitive shifts, supply-chain updates, talent-market news, and any macro signals that could influence the initiative. Deliver a situational briefing that surfaces emerging risks, external dependencies, and windows of opportunity for the leadership team."
            + " Use the available tools thoughtfully: rely on `get_global_news` for broad coverage, call `get_news` when you need focused intelligence, and reserve Alpha Vantage finance calls for requests that explicitly require capital-markets confirmation."
            + " Finish with a Markdown table summarising each external factor, its potential impact, and recommended monitoring or mitigation steps."
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
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
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
            "news_report": report,
        }

    return news_analyst_node
