import time
import json


def create_risk_manager(llm, memory):
    def risk_manager_node(state) -> dict:

        company_name = state["company_of_interest"]

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        market_research_report = state["market_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]
        sentiment_report = state["sentiment_report"]
        trader_plan = state["investment_plan"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are the Risk & External Integration Lead. Review the debate among the three risk posture advocates—Bold, Balanced, and Guarded—and determine the organisational stance the executive team should take next. Your output must land on one of three actions: ADVANCE, MAINTAIN, or REASSESS. Only recommend MAINTAIN if it is explicitly justified by the arguments presented; otherwise commit to moving forward or rethinking.

Guidelines for Decision-Making:
1. **Surface the Strongest Arguments**: Capture the critical insights from each analyst, emphasising relevance to {company_name}'s near-term outlook.
2. **Connect to Execution**: Start with the coordination plan, **{trader_plan}**, and refine it to address the highlighted risks and opportunities.
3. **Apply Organisational Memory**: Draw on the following prior lessons to avoid repeating mistakes and to reinforce proven mitigations: {past_memory_str}
4. **Stay Source-Aware**: If the debate references financial-market data, note whether it stemmed from Alpha Vantage or other sources; otherwise prioritise Google and LLM-derived intelligence when summarising.

Deliverables:
- A decisive recommendation labelled as FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS**.
- Supporting rationale that references key debate moments, operational implications, and mitigation steps.

---

**Risk Debate History:**
{history}

---

Be decisive, integrative, and improvement-oriented. Highlight how the organisation should respond immediately and what must be monitored next."""

        response = llm.invoke(prompt)

        new_risk_debate_state = {
            "judge_decision": response.content,
            "history": risk_debate_state["history"],
            "risky_history": risk_debate_state["risky_history"],
            "safe_history": risk_debate_state["safe_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_risky_response": risk_debate_state["current_risky_response"],
            "current_safe_response": risk_debate_state["current_safe_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }

        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": response.content,
        }

    return risk_manager_node
