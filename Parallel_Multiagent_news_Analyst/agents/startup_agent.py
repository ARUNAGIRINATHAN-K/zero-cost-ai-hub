from langchain_groq import ChatGroq
from tools.tavily_search import search_news, build_article_digest
from tools.reliability import run_with_retries
from prompts.startup_prompt import STARTUP_PROMPT

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def startup_agent(state):
    """
    Startup & Venture Capital News Agent

    Responsibilities:
    - Search startup ecosystem news
    - Track funding rounds and acquisitions
    - Monitor emerging tech startups
    - Analyze venture capital trends
    """

    query = state["query"]
    model="llama-3.3-70b-versatile",
    # Startup-focused search query
    startup_query = f"""
    {query}
    startups
    venture capital
    funding rounds
    acquisitions
    unicorn startups
    SaaS
    AI startups
    tech founders
    startup ecosystem
    """

    # Search latest startup news
    search_results = search_news(startup_query, max_results=3)
    combined_articles = build_article_digest(search_results)

    # Generate startup ecosystem summary
    response = run_with_retries(
        lambda: llm.invoke(
            STARTUP_PROMPT.format(
                query=query,
                articles=combined_articles
            )
        ),
        fallback="Unable to generate a startup summary right now.",
        label="Startup agent LLM",
        retries=2,
        timeout_seconds=60,
        backoff_seconds=1.5,
    )

    summary = response.content if hasattr(response, "content") else response

    return {
        "startup_results": [
            {
                "agent": "Startup Agent",
                "summary": summary,
                "sources": [
                    r.get("url") for r in search_results
                ]
            }
        ]
    }