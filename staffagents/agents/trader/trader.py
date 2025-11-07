import functools
import time
import json


def create_trader(llm, memory):
    def trader_node(state, name):
        company_name = state["company_of_interest"]
        investment_plan = state["investment_plan"]
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        if past_memories:
            for i, rec in enumerate(past_memories, 1):
                past_memory_str += rec["recommendation"] + "\n\n"
        else:
            past_memory_str = "No past memories found."

        context = {
            "role": "user",
            "content": (
                "Your cross-functional staff council has aligned on the following integrated plan for "
                f"{company_name}. It blends strategic signals, operational capacity, customer sentiment, and external risk intelligence."
                " Use it as the baseline for your leadership recommendation.\n\n"
                f"Integrated Initiative Blueprint: {investment_plan}\n\n"
                "Translate this plan into clear next actions for the executive team."
            ),
        }

        messages = [
            {
                "role": "system",
                "content": (
                    "You are the Staff Coordination Lead, responsible for synthesising multi-analyst input into a concrete organisational recommendation."
                    " Outline decisive next steps, key owners, and immediate checkpoints."
                    " Close with a firm call using the format 'FINAL STAFF RECOMMENDATION: **ADVANCE/MAINTAIN/REASSESS**'."
                    " Use lessons from prior reflections to avoid repeating mistakes and to emphasise organisational learning."
                    f" Here are relevant past reflections to inform your reasoning: {past_memory_str}"
                ),
            },
            context,
        ]

        result = llm.invoke(messages)

        return {
            "messages": [result],
            "trader_investment_plan": result.content,
            "sender": name,
        }

    return functools.partial(trader_node, name="Trader")
