from langchain_groq import ChatGroq
from tools.tavily_search import search_news, build_article_digest
from tools.reliability import run_with_retries
from prompts.finance_prompt import FINANCE_PROMPT

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def finance_agent(state):
    """
    Finance News Agent

    Responsibilities:
    - Search latest finance news
    - Analyze stock market trends
    - Summarize economic insights
    - Return structured finance briefing
    """

    query = state["query"]
    model="llama-3.3-70b-versatile",
    # Enhanced finance-focused search query
    finance_query = f"""
    {query}
    latest finance news
    stock market
    economy
    business trends
    investments
    """

    # Search news using Tavily
    search_results = search_news(finance_query, max_results=3)
    combined_articles = build_article_digest(search_results)

    # Generate finance summary
    response = run_with_retries(
        lambda: llm.invoke(
            FINANCE_PROMPT.format(
                query=query,
                articles=combined_articles
            )
        ),
        fallback="Unable to generate a finance summary right now.",
        label="Finance agent LLM",
        retries=2,
        timeout_seconds=60,
        backoff_seconds=1.5,
    )

    summary = response.content if hasattr(response, "content") else response

    return {
        "finance_results": [
            {
                "agent": "Finance Agent",
                "summary": summary,
                "sources": [
                    r.get("url") for r in search_results
                ]
            }
        ]
    }