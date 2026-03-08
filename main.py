from fastapi import FastAPI
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title = "Semantic Diff Reviewer", description = "Semantic Diff Reviewer is an AI-powered code review assistant for GitHub Pull Requests. It analyzes modified functions, traces dependency impact, and uses an LLM to identify architectural risks, hidden regressions, and potential breaking changes.")

@app.on_event("startup")
async def startup_event() -> None:
      logging.info("Starting up Semantic Diff Reviewer")

@app.get("/health")
async def health() -> Dict[str, str]:
      return {"status": "ok"}
