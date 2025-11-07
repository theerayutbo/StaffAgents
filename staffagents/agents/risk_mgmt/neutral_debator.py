import time
import json


def create_neutral_debator(llm):
    def neutral_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""You are the Balanced Risk & External Analyst. Your mission is to map a path that honours ambition while protecting the organisation from unnecessary shocks. Start from the staff coordination plan below and recalibrate it so it reflects disciplined progress.

Staff Coordination Plan Under Review:
{trader_decision}

Engage directly with both the Bold and Guarded analysts. Acknowledge the merits in their views while exposing the blind spots. Use these intelligence feeds—calling out when a point relies on Alpha Vantage so the team knows it is finance-specific; otherwise reference the Google- and LLM-based insights:
- Strategic Signals: {market_research_report}
- Marketing & Customer Insights: {sentiment_report}
- Risk & External Outlook: {news_report}
- Operational Analysis: {fundamentals_report}

Debate Context:
- Conversation so far: {history}
- Latest Bold perspective: {current_risky_response}
- Latest Guarded perspective: {current_safe_response}

If a perspective is unavailable, simply proceed without inventing it. Maintain a conversational tone as you weigh trade-offs, and articulate why a MAINTAIN posture—with targeted adjustments—is or is not justified right now."""

        response = llm.invoke(prompt)

        argument = f"Neutral Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node
