#!/usr/bin/env python3
"""
run_backend.py: Start FastAPI server for PyLintPro linting API.
"""

import os
import sys
from pathlib import Path
import logging

# Ensure project root on path for imports
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # Prepend project root to sys.path  [oai_citation_attribution:5‡Python documentation](https://docs.python.org/3/library/sys_path_init.html?utm_source=chatgpt.com)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.lint import lint_code
from src.utils import parse_flake8_output

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)  # Basic logging setup  [oai_citation_attribution:6‡Python documentation](https://docs.python.org/3/library/logging.html?utm_source=chatgpt.com)
logger = logging.getLogger("run_backend")

# Pydantic models for request/response
class LintRequest(BaseModel):
    code: str  # Incoming Python code


class Issue(BaseModel):
    file: str
    line: int
    column: int
    code: str
    message: str


class LintResponse(BaseModel):
    formatted_code: str
    issues: list[Issue]


# FastAPI application instance
app = FastAPI(
    title="PyLintPro Backend API",
    description="API for linting and formatting Python code",
    version="1.0.0"
)  # FastAPI setup  [oai_citation_attribution:7‡FastAPI](https://fastapi.tiangolo.com/?utm_source=chatgpt.com)

# Enable CORS for all origins (adjust in production)  [oai_citation_attribution:8‡FastAPI](https://fastapi.tiangolo.com/tutorial/cors/?utm_source=chatgpt.com)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "service": "PyLintPro Backend API"}  # Basic GET route  [oai_citation_attribution:9‡FastAPI](https://fastapi.tiangolo.com/tutorial/?utm_source=chatgpt.com)

@app.post("/lint", response_model=LintResponse)
def lint_endpoint(request: LintRequest):
    """
    Lint and format provided Python code.
    """
    logger.info("Received lint request: %d characters", len(request.code))
    try:
        result = lint_code(request.code)
        # Split formatted code and issues
        if "# Flake8 issues:" in result:
            formatted, issues_str = result.split("# Flake8 issues:\n", 1)
        else:
            formatted, issues_str = result, ""
        issues = parse_flake8_output(issues_str)
        return LintResponse(formatted_code=formatted, issues=issues)
    except Exception as e:
        logger.error("Error during linting: %s", e, exc_info=True)
        # Return a 500 error on failure  [oai_citation_attribution:10‡FastAPI](https://fastapi.tiangolo.com/tutorial/handling-errors/?utm_source=chatgpt.com)
        raise HTTPException(status_code=500, detail="Internal linting error")

if __name__ == "__main__":
    # Protect entry point to avoid recursive spawning  [oai_citation_attribution:11‡Stack Overflow](https://stackoverflow.com/questions/73908734/how-to-run-uvicorn-fastapi-server-as-a-module-from-another-python-file?utm_source=chatgpt.com)
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info("Starting PyLintPro backend on %s:%d", host, port)
    uvicorn.run("scripts.run_backend:app", host=host, port=port, log_level="info")  # Run with Uvicorn  [oai_citation_attribution:12‡FastAPI](https://fastapi.tiangolo.com/deployment/manually/?utm_source=chatgpt.com)
