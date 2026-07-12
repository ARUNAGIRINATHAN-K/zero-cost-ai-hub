from langchain_groq import ChatGroq
from tools.tavily_search import search_news, build_article_digest
from tools.reliability import run_with_retries
from prompts.cyber_prompt import CYBER_PROMPT

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def cyber_agent(state):
    """
    Cybersecurity News Agent

    Responsibilities:
    - Search latest cybersecurity news
    - Monitor cyberattacks and data breaches
    - Track malware/ransomware campaigns
    - Analyze threat intelligence trends
    """

    query = state["query"]
    model="llama-3.3-70b-versatile",
    # Cybersecurity-focused search query
    cyber_query = f"""
    {query}
    cybersecurity
    cyber attack
    ransomware
    malware
    data breach
    zero day vulnerability
    threat intelligence
    phishing
    cloud security
    """

    # Search latest cybersecurity news
    search_results = search_news(cyber_query, max_results=3)
    combined_articles = build_article_digest(search_results)

    # Generate cybersecurity analysis summary
    response = run_with_retries(
        lambda: llm.invoke(
            CYBER_PROMPT.format(
                query=query,
                articles=combined_articles
            )
        ),
        fallback="Unable to generate a cybersecurity summary right now.",
        label="Cyber agent LLM",
        retries=2,
        timeout_seconds=60,
        backoff_seconds=1.5,
    )

    summary = response.content if hasattr(response, "content") else response

    return {
        "cyber_results": [
            {
                "agent": "Cybersecurity Agent",
                "summary": summary,
                "sources": [
                    r.get("url") for r in search_results
                ]
            }
        ]
    }