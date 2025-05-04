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
sys.path.insert(0, str(ROOT))

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
)
logger = logging.getLogger("run_backend")

class LintRequest(BaseModel):
    """
    Pydantic model for lint request.
    """
    code: str

class Issue(BaseModel):
    """
    Pydantic model for lint issue.
    """
    file: str
    line: int
    column: int
    code: str
    message: str

class LintResponse(BaseModel):
    """
    Pydantic model for lint response.
    """
    formatted_code: str
    issues: list[Issue]

app = FastAPI(
    title="PyLintPro Backend API",
    description="API for linting and formatting Python code",
    version="1.0.0"
)

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
    return {"status": "ok", "service": "PyLintPro Backend API"}

@app.post("/lint", response_model=LintResponse)
def lint_endpoint(request: LintRequest):
    """
    Lint and format provided Python code.
    """
    logger.info("Received lint request: %d characters", len(request.code))
    try:
        result = lint_code(request.code)
        if "# Flake8 issues:" in result:
            formatted, issues_str = result.split("# Flake8 issues:\n", 1)
        else:
            formatted, issues_str = result, ""
        issues = parse_flake8_output(issues_str)
        return LintResponse(formatted_code=formatted, issues=issues)
    except Exception as e:
        logger.error("Error during linting: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal linting error")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info("Starting PyLintPro backend on %s:%d", host, port)
    uvicorn.run("scripts.run_backend:app", host=host, port=port, log_level="info")
