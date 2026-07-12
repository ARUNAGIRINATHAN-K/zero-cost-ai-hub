from typing import TypedDict, List, Dict, Any
from typing_extensions import Annotated
import operator


class NewsState(TypedDict):
    """
    Shared state across all agents in the LangGraph workflow.
    """

    # =========================================================
    # USER INPUT
    # =========================================================

    query: str

    # =========================================================
    # AGENT RESULTS
    # Using Annotated + operator.add allows
    # parallel agent outputs to merge automatically.
    # =========================================================

    finance_results: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    ai_results: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    cyber_results: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    startup_results: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    # =========================================================
    # FINAL MERGED REPORT
    # =========================================================

    final_report: str