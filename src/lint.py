# src/lint.py
"""
Linting module for PyLintPro
"""

import tempfile
import os
import subprocess
import autopep8


def lint_code(code: str) -> str:
    """
    Formats Python code with autopep8 and runs flake8 to collect linting issues.
    
    Args:
        code (str): The Python source code to lint.

    Returns:
        str: The formatted code with flake8 issues appended as comments.
    """
    # Format with autopep8, fall back to original code on failure
    try:
        formatted_code = autopep8.fix_code(code, options={"aggressive": 1})
    except Exception as e:
        print(f"Warning: autopep8 formatting failed ({e}), using original code")
        formatted_code = code

    # Write to a temporary file for flake8
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
        tmp.write(formatted_code)
        tmp_path = tmp.name

    # Run flake8
    result = subprocess.run(
        ["flake8", tmp_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Clean up temp file
    os.unlink(tmp_path)

    issues = result.stdout.strip() or "No issues found."
    return f"{formatted_code}\n\n# Flake8 issues: {issues}"
