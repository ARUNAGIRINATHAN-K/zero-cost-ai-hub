from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Any
import uvicorn

# Import workflow runner
from graph.workflow import run_news_analysis

# =========================================================
# INITIALIZE FASTAPI
# =========================================================

app = FastAPI(
    title="Parallel Multi-Agent News Analyst",
    description="""
    Real-time Multi-Agent AI News Analysis System
    powered by LangGraph, Groq, and Tavily.
    """,
    version="1.0.0"
)

# =========================================================
# REQUEST MODEL
# =========================================================

class NewsRequest(BaseModel):
    query: str


class AgentItem(BaseModel):
    agent: Optional[str] = None
    summary: Optional[str] = None
    sources: Optional[List[Any]] = None


class AnalyzeResponse(BaseModel):
    success: bool = True
    query: str
    final_report: Optional[str] = None
    finance_results: Optional[List[AgentItem]] = None
    ai_results: Optional[List[AgentItem]] = None
    cyber_results: Optional[List[AgentItem]] = None
    startup_results: Optional[List[AgentItem]] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: int
    details: Optional[Any] = None


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Parallel Multi-Agent News Analyst API",
        "status": "running",
        "framework": "LangGraph",
        "llm": "Groq",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# =========================================================
# NEWS ANALYSIS ENDPOINT
# =========================================================

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "code": exc.status_code},
    )


@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "details": str(exc),
        },
    )


@app.post("/analyze", response_model=AnalyzeResponse, responses={400: {"model": ErrorResponse}, 503: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def analyze_news(request: NewsRequest):
    # Validate
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`query` must be a non-empty string")

    try:
        result = run_news_analysis(query=request.query)

        return AnalyzeResponse(
            success=True,
            query=request.query,
            final_report=result.get("final_report"),
            finance_results=result.get("finance_results"),
            ai_results=result.get("ai_results"),
            cyber_results=result.get("cyber_results"),
            startup_results=result.get("startup_results"),
        )

    except Exception as e:
        msg = str(e)
        # Map upstream errors to 503 where possible
        if any(k in msg.lower() for k in ("groq", "tavily", "timeout", "connection")):
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Upstream service error")
        raise


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )