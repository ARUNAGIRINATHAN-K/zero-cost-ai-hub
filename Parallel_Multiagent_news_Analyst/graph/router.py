from langgraph.constants import Send
from graph.state import NewsState


def router(state: NewsState):
    """
    Router Function

    Uses LangGraph Send API to fan out
    multiple specialized agents in parallel.

    Each agent receives the same shared state.
    """

    return [

        # Finance Analysis Agent
        Send(
            "finance_agent",
            state
        ),

        # AI Industry Analysis Agent
        Send(
            "ai_agent",
            state
        ),

        # Cybersecurity Threat Analysis Agent
        Send(
            "cyber_agent",
            state
        ),

        # Startup & VC Ecosystem Agent
        Send(
            "startup_agent",
            state
        ),
    ]