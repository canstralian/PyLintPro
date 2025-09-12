# src/config.py

from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths to configuration files
FLAKE8_CONFIG = BASE_DIR / ".flake8"
PYPROJECT_TOML = BASE_DIR / "pyproject.toml"

# Default linting settings
DEFAULT_MAX_LINE_LENGTH = 88
DEFAULT_IGNORE_RULES = ["E203", "W503"]  # To align with Black formatting

# Application metadata
APP_NAME = "PyLintPro"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = ("A Gradio app that helps users improve Python code to "
                   "meet Flake8 and PEP 8 standards.")

# Gradio interface settings
GRADIO_THEME = "default"
GRADIO_CSS = ".gradio-container { padding: 2rem; }"
