from fastapi import FastAPI, Header, HTTPException, Request
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title = "Semantic Diff Reviewer", description = "Semantic Diff Reviewer is an AI-powered code review assistant for GitHub Pull Requests. It analyzes modified functions, traces dependency impact, and uses an LLM to identify architectural risks, hidden regressions, and potential breaking changes.")

@app.on_event("startup")
async def startup_event() -> None:
      logger.info("Starting up Semantic Diff Reviewer")

@app.get("/health")
async def health() -> Dict[str, str]:
      return {"status": "ok"}
@app.post("/webhook")
async def github_webhook(
      request: Request,
      x_github_event: str = Header(default="unknown",alias="X-GitHub-Event")
) -> Dict[str, str]:
      try:
            payload = await request.json()
      except Exception as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc
      repository = payload.get("repository", {}).get("full_name", "unknown")
      pr_number = payload.get("pull_request", {}).get("number")
      logger.info(
            "Received GitHub event=%s repository=%s pr_number=%s",
            x_github_event,
            repository,
            pr_number)
      return {"status": "received"} 