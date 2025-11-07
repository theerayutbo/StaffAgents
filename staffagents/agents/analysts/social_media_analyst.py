from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from staffagents.agents.utils.agent_utils import get_news
from staffagents.dataflows.config import get_config


def create_social_media_analyst(llm):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_news,
        ]

        system_message = (
            "You are the Marketing & Customer Analyst within the StaffAgents ensemble. Review social conversations, customer feedback, campaign chatter, and frontline experience over the past week to explain how audiences feel about the initiative. Translate observations into actionable implications for go-to-market, service delivery, and community management."
            + " Make sure the narrative pairs qualitative insight with crisp evidence—quotes, trend summaries, sentiment movements—and close with a Markdown table that spotlights key signals, source channels, and follow-up actions."
            + " Default to Google-sourced intelligence and your own reasoning. Only reach for Alpha Vantage finance tooling if the question explicitly turns to financial sentiment; otherwise emphasise customer and market-perception data."
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
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
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
            "sentiment_report": report,
        }

    return social_media_analyst_node
