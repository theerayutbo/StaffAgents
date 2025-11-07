# staffagents/graph/signal_processing.py

from langchain_openai import ChatOpenAI


class SignalProcessor:
    """Processes StaffAgents signals to extract actionable organisational decisions."""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """Initialize with an LLM for processing."""
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """Process a full StaffAgents signal to extract the core decision.

        Args:
            full_signal: Complete decision narrative produced by the agents.

        Returns:
            Extracted decision (ADVANCE, MAINTAIN, or REASSESS)
        """
        messages = [
            (
                "system",
                "You are an efficient assistant designed to review StaffAgents collaboration transcripts. Extract the organisational decision—ADVANCE, MAINTAIN, or REASSESS—from the provided narrative. Respond with exactly one of these words and nothing else.",
            ),
            ("human", full_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
