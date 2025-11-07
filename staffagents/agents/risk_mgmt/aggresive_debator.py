import time
import json


def create_risky_debator(llm):
    def risky_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        risky_history = risk_debate_state.get("risky_history", "")

        current_safe_response = risk_debate_state.get("current_safe_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""You are the Bold Risk & External Analyst. Champion decisive moves that unlock outsized upside while acknowledging the safeguards needed to absorb volatility. Build on the staff coordination plan below and emphasise how moving quickly advances organisational goals.

Staff Coordination Plan Under Review:
{trader_decision}

Directly address the Guarded and Balanced analysts. Challenge their caution with data-backed optimism, calling out where restraint would cause missed opportunities. Use the following intelligence to anchor your arguments (call out explicitly when a data point comes from Alpha Vantage—only bring those in when a finance-specific question is in play; otherwise rely on Google- and LLM-derived context):
- Strategic Signals: {market_research_report}
- Marketing & Customer Insights: {sentiment_report}
- Risk & External Outlook: {news_report}
- Operational Analysis: {fundamentals_report}

Debate Context:
- Conversation so far: {history}
- Latest Guarded perspective: {current_safe_response}
- Latest Balanced perspective: {current_neutral_response}

If any perspective is missing, do not fabricate it—advance your viewpoint with the information available. Be energetic, persuasive, and conversational, keeping the focus on why a bold ADVANCE posture is justified right now."""

        response = llm.invoke(prompt)

        argument = f"Risky Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risky_history + "\n" + argument,
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Risky",
            "current_risky_response": argument,
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return risky_node
