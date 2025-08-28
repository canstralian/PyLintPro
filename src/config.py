# src/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths to configuration files
FLAKE8_CONFIG = BASE_DIR / ".flake8"
PYPROJECT_TOML = BASE_DIR / "pyproject.toml"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mendicant:password@localhost:5432/mendicant_dev")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# GitHub App Configuration
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

# API Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Default linting settings
DEFAULT_MAX_LINE_LENGTH = 88
DEFAULT_IGNORE_RULES = ["E203", "W503"]  # To align with Black formatting

# Application metadata
APP_NAME = "Mendicant AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Self-healing repositories that automatically detect and fix broken window issues."

# Gradio interface settings
GRADIO_THEME = "default"
GRADIO_CSS = ".gradio-container { padding: 2rem; }"

# Repository Health Check Configuration
HEALTH_CHECK_CATEGORIES = [
    "code_quality",
    "security", 
    "testing",
    "documentation",
    "dependencies",
    "performance"
]

# Security scanning settings
SECURITY_SCANNER_API_KEY = os.getenv("SECURITY_SCANNER_API_KEY")

# Monitoring Configuration
OPENTELEMETRY_ENDPOINT = os.getenv("OPENTELEMETRY_ENDPOINT")
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Pilot Program Configuration
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
PILOT_PRICE_ID = os.getenv("PILOT_PRICE_ID")
PILOT_PRICE = 1500  # $1,500 for 14-day pilot

# Public Commitment Tracking
MRR_TARGET = 10000  # $10k MRR target
PILOT_TARGET = 10
OUTREACH_TARGET = 500
INTERVIEW_TARGET = 50
INSTALLATION_TARGET = 25