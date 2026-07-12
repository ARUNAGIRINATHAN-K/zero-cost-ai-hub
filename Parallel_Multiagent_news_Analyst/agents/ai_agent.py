from langchain_groq import ChatGroq
from tools.tavily_search import search_news, build_article_digest
from tools.reliability import run_with_retries
from prompts.ai_prompt import AI_PROMPT

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def ai_agent(state):
    """
    AI News Agent

    Responsibilities:
    - Search latest AI/LLM news
    - Track foundation model updates
    - Monitor AI startups and releases
    - Summarize AI industry trends
    """

    query = state["query"]
    model="llama-3.3-70b-versatile",
    # AI-focused search query
    ai_query = f"""
    {query}
    artificial intelligence
    generative AI
    LLM
    machine learning
    OpenAI
    Anthropic
    Google DeepMind
    AI startups
    """

    # Search latest AI news
    search_results = search_news(ai_query, max_results=3)
    combined_articles = build_article_digest(search_results)

    # Generate AI analysis summary
    response = run_with_retries(
        lambda: llm.invoke(
            AI_PROMPT.format(
                query=query,
                articles=combined_articles
            )
        ),
        fallback="Unable to generate an AI summary right now.",
        label="AI agent LLM",
        retries=2,
        timeout_seconds=60,
        backoff_seconds=1.5,
    )

    summary = response.content if hasattr(response, "content") else response

    return {
        "ai_results": [
            {
                "agent": "AI Agent",
                "summary": summary,
                "sources": [
                    r.get("url") for r in search_results
                ]
            }
        ]
    }