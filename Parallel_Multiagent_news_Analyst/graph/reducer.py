from graph.state import NewsState


def _latest_summary(items):
    if not items:
        return "No results available."

    summary = items[-1].get("summary")
    return summary or "No summary available."


def _latest_sources(items):
    if not items:
        return []

    sources = items[-1].get("sources") or []
    return [s for s in sources if s]


def reducer(state: NewsState):
    """
    Merge the parallel agent outputs into a single final report.
    """

    finance_summary = _latest_summary(state.get("finance_results", []))
    ai_summary = _latest_summary(state.get("ai_results", []))
    cyber_summary = _latest_summary(state.get("cyber_results", []))
    startup_summary = _latest_summary(state.get("startup_results", []))

    final_report = f"""## Final Intelligence Briefing

### Finance
{finance_summary}

Sources:
{('\n'.join([f'- {s}' for s in _latest_sources(state.get("finance_results", []))]) or 'No sources available.')}

### AI
{ai_summary}

Sources:
{('\n'.join([f'- {s}' for s in _latest_sources(state.get("ai_results", []))]) or 'No sources available.')}

### Cybersecurity
{cyber_summary}

Sources:
{('\n'.join([f'- {s}' for s in _latest_sources(state.get("cyber_results", []))]) or 'No sources available.')}

### Startups
{startup_summary}

Sources:
{('\n'.join([f'- {s}' for s in _latest_sources(state.get("startup_results", []))]) or 'No sources available.')}
"""

    return {
        "final_report": final_report.strip()
    }