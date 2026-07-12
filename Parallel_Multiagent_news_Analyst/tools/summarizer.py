import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables."
    )

# =========================================================
# INITIALIZE LLM
# =========================================================

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)

# =========================================================
# DEFAULT SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are an expert AI News Summarizer.

Your responsibilities:
- Summarize news clearly and concisely
- Extract key insights
- Highlight important developments
- Identify risks and opportunities
- Maintain professional tone

Always provide:
1. Key Headlines
2. Important Insights
3. Market/Industry Impact
4. Final Summary
"""

# =========================================================
# GENERIC SUMMARIZER FUNCTION
# =========================================================

def summarize_news(
    topic: str,
    articles: str
):
    """
    Generate AI-powered summaries for news articles.

    Args:
        topic (str):
            News topic

        articles (str):
            Combined article content

    Returns:
        str:
            Summarized output
    """

    prompt = f"""
    {SYSTEM_PROMPT}

    Topic:
    {topic}

    Articles:
    {articles}

    Generate a concise analytical summary.
    """

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        model="llama-3.3-70b-versatile",

        return "Failed to generate summary."


# =========================================================
# SPECIALIZED SUMMARIZERS
# =========================================================

def summarize_finance_news(articles: str):

    finance_prompt = f"""
    You are a Financial Market Analyst.

    Analyze:
    - stock market movements
    - economic signals
    - investment trends
    - risks and opportunities

    Articles:
    {articles}
    """

    response = llm.invoke(finance_prompt)

    return response.content


def summarize_ai_news(articles: str):

    ai_prompt = f"""
    You are an AI Industry Analyst.

    Analyze:
    - LLM developments
    - AI startups
    - enterprise adoption
    - emerging AI trends

    Articles:
    {articles}
    """

    response = llm.invoke(ai_prompt)

    return response.content


def summarize_cyber_news(articles: str):

    cyber_prompt = f"""
    You are a Cybersecurity Threat Intelligence Analyst.

    Analyze:
    - ransomware attacks
    - malware campaigns
    - vulnerabilities
    - threat intelligence trends

    Articles:
    {articles}
    """

    response = llm.invoke(cyber_prompt)

    return response.content


def summarize_startup_news(articles: str):

    startup_prompt = f"""
    You are a Startup & Venture Capital Analyst.

    Analyze:
    - startup funding
    - acquisitions
    - VC trends
    - innovation opportunities

    Articles:
    {articles}
    """

    response = llm.invoke(startup_prompt)

    return response.content


# =========================================================
# TEST RUN
# =========================================================

if __name__ == "__main__":

    sample_articles = """
    OpenAI released a new enterprise AI model.
    Several AI startups raised significant funding.
    Cybersecurity firms reported new ransomware threats.
    """

    summary = summarize_news(
        topic="AI & Cybersecurity",
        articles=sample_articles
    )

    print("\n" + "=" * 60)
    print("AI GENERATED SUMMARY")
    print("=" * 60)

    print(summary)