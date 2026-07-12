from langgraph.graph import StateGraph, END
from langgraph.constants import Send

# Import shared state
from graph.state import NewsState

# Import agents
from agents.finance_agent import finance_agent
from agents.ai_agent import ai_agent
from agents.cyber_agent import cyber_agent
from agents.startup_agent import startup_agent

# Import reducer
from graph.reducer import reducer


# =========================================================
# ROUTER FUNCTION
# =========================================================

def router(state: NewsState):
    """
    Fan-out router using LangGraph Send API.

    Launches all agents in parallel.
    """

    return [
        Send("finance_agent", state),
        Send("ai_agent", state),
        Send("cyber_agent", state),
        Send("startup_agent", state),
    ]


# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(NewsState)

# Add Agent Nodes
builder.add_node("finance_agent", finance_agent)
builder.add_node("ai_agent", ai_agent)
builder.add_node("cyber_agent", cyber_agent)
builder.add_node("startup_agent", startup_agent)

# Add Reducer Node
builder.add_node("reducer", reducer)

# =========================================================
# PARALLEL ENTRY POINT
# =========================================================

builder.set_conditional_entry_point(router)

# =========================================================
# CONNECT AGENTS TO REDUCER
# =========================================================

builder.add_edge("finance_agent", "reducer")
builder.add_edge("ai_agent", "reducer")
builder.add_edge("cyber_agent", "reducer")
builder.add_edge("startup_agent", "reducer")

# =========================================================
# FINAL EDGE
# =========================================================

builder.add_edge("reducer", END)

# =========================================================
# COMPILE GRAPH
# =========================================================

graph = builder.compile()


# =========================================================
# EXECUTION FUNCTION
# =========================================================

def run_news_analysis(query: str):
    """
    Execute the Parallel Multi-Agent News Analyst
    """

    initial_state = {
        "query": query,
        "finance_results": [],
        "ai_results": [],
        "cyber_results": [],
        "startup_results": [],
        "final_report": "",
    }

    result = graph.invoke(initial_state)

    return result


# =========================================================
# TEST RUN
# =========================================================

if __name__ == "__main__":

    response = run_news_analysis(
        "Latest AI, finance, cybersecurity, and startup news"
    )

    print("\n" + "=" * 60)
    print("PARALLEL MULTI-AGENT NEWS ANALYST")
    print("=" * 60)

    print("\nFINAL REPORT:\n")
    print(response["final_report"])