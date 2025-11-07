from langchain_core.messages import AIMessage
import time
import json


def create_bear_researcher(llm, memory):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are the Challenge Sentinel. Build a rigorous case for why the organisation should REASSESS or slow the initiative. Spotlight the hidden costs, friction points, and external headwinds that could derail success if left unchecked.

Direct your analysis toward:
- Structural Risks: Identify operational, financial, or compliance vulnerabilities.
- Competitive and Market Threats: Surface forces that could erode advantage or momentum.
- Negative Signals: Call out concerning metrics, sentiment dips, or adverse news.
- Opportunity Counterpoints: Deconstruct the Opportunity Advocate's latest argument, showing where optimism glosses over material risk.
- Learning Loop: Reference historical lessons to avoid repeating painful outcomes.

Intelligence at your disposal:
- Strategic Signals: {market_research_report}
- Marketing & Customer Insights: {sentiment_report}
- Risk & External Outlook: {news_report}
- Operational Analysis: {fundamentals_report}
- Debate history: {history}
- Most recent Opportunity Advocate argument: {current_response}
- Prior reflections: {past_memory_str}

Deliver your analysis conversationally yet firmly, keeping the spotlight on why caution or a REASSESS stance protects the organisation's long-term position."""

        response = llm.invoke(prompt)

        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bear_history": bear_history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node
