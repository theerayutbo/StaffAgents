import time
import json


def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are the Research Council Chair. Reconcile the perspectives from the Opportunity Advocate and the Challenge Sentinel, then chart a unified organisational plan. Land on one of three pathways—ADVANCE, MAINTAIN, or REASSESS—and explain how the debate evidence leads to that choice. Avoid picking MAINTAIN unless it is explicitly earned by the arguments.

Your deliverable must include:
- **Decision Call**: State your stance with the phrasing FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS**.
- **Strategic Narrative**: Summarise the most compelling bullish and cautious evidence and how it shapes the recommendation.
- **Coordinated Action Plan**: Provide concrete next steps, accountable owners, success metrics, and immediate checkpoints the staff coordination lead can execute.
- **Learning Integration**: Weave in lessons from previous reflections to demonstrate how the team is improving. Past insights to reference:\n"{past_memory_str}"

Debate Transcript:
{history}

Write conversationally but decisively so the rest of the organisation can act without ambiguity."""
        response = llm.invoke(prompt)

        new_investment_debate_state = {
            "judge_decision": response.content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response.content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response.content,
        }

    return research_manager_node
