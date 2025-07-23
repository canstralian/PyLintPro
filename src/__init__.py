# src/__init__.py

"""
PyLintPro
A Gradio application to lint and format Python code according to PEP 8
and Flake8 standards.
"""

__version__ = "1.0.0"

from .config import (
    BASE_DIR,
    FLAKE8_CONFIG,
    PYPROJECT_TOML,
    DEFAULT_MAX_LINE_LENGTH,
    DEFAULT_IGNORE_RULES,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    GRADIO_THEME,
    GRADIO_CSS,
)
from .lint import lint_code
from .utils import (
    safe_run,
    parse_flake8_output,
    format_issues_for_display,
    load_examples,
    load_yaml_config,
    setup_logging,
)

__all__ = [
    "lint_code",
    "safe_run",
    "parse_flake8_output",
    "format_issues_for_display",
    "load_examples",
    "load_yaml_config",
    "setup_logging",
    "BASE_DIR",
    "FLAKE8_CONFIG",
    "PYPROJECT_TOML",
    "DEFAULT_MAX_LINE_LENGTH",
    "DEFAULT_IGNORE_RULES",
    "APP_NAME",
    "APP_VERSION",
    "APP_DESCRIPTION",
    "GRADIO_THEME",
    "GRADIO_CSS",
]
