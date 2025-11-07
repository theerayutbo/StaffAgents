from langchain_core.messages import AIMessage
import time
import json


def create_safe_debator(llm):
    def safe_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        safe_history = risk_debate_state.get("safe_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""You are the Guarded Risk & External Analyst. Safeguard the organisation by stress-testing every assumption in the staff coordination plan below. Focus on where execution could fail, where external threats might erupt, and which contingencies must be activated.

Staff Coordination Plan Under Review:
{trader_decision}

Engage the Bold and Balanced analysts directly—acknowledge any strong points they make, but emphasise the hazards they are neglecting. Use the intelligence packet below, flagging when a data point comes from Alpha Vantage so the team knows it ties to finance; otherwise rely on Google- and LLM-driven context:
- Strategic Signals: {market_research_report}
- Marketing & Customer Insights: {sentiment_report}
- Risk & External Outlook: {news_report}
- Operational Analysis: {fundamentals_report}

Debate Context:
- Conversation so far: {history}
- Latest Bold perspective: {current_risky_response}
- Latest Balanced perspective: {current_neutral_response}

If a perspective is missing, simply proceed without inventing it. Keep your tone conversational yet firm as you argue for a REASSESS posture unless credible mitigations are in place."""

        response = llm.invoke(prompt)

        argument = f"Safe Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": safe_history + "\n" + argument,
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Safe",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": argument,
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return safe_node
