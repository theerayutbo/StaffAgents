from langchain_core.messages import AIMessage
import time
import json


def create_bull_researcher(llm, memory):
    def bull_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bull_history = investment_debate_state.get("bull_history", "")

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

        prompt = f"""You are the Opportunity Advocate. Paint an inspiring yet grounded case for why the organisation should ADVANCE with the initiative. Demonstrate how the data points to momentum, differentiation, and stakeholder enthusiasm that outweigh the risks.

Anchor your contribution around:
- Expansion Potential: Spotlight opportunities to grow impact, revenue, or mission outcomes.
- Strategic Differentiators: Highlight unique capabilities, partnerships, or timing advantages the organisation holds.
- Positive Indicators: Leverage operational health, market tailwinds, customer sentiment, and external signals.
- Challenge Response: Engage directly with the Challenge Sentinel's latest critique, dismantling concerns with evidence and practical mitigations.
- Learning Loop: Reference the lessons below to show how past experiences inform today's bolder stance.

Intelligence at your disposal:
- Strategic Signals: {market_research_report}
- Marketing & Customer Insights: {sentiment_report}
- Risk & External Outlook: {news_report}
- Operational Analysis: {fundamentals_report}
- Debate history: {history}
- Most recent Challenge Sentinel argument: {current_response}
- Prior reflections: {past_memory_str}

Present your case conversationally and energetically, weaving the data into a persuasive narrative that rallies the council around forward motion."""

        response = llm.invoke(prompt)

        argument = f"Bull Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bull_history": bull_history + "\n" + argument,
            "bear_history": investment_debate_state.get("bear_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bull_node
