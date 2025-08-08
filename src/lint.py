"""
Linting module for PyLintPro
"""

import autopep8
import tempfile
import os
import subprocess


def lint_code(code):
    """
    Formats code with autopep8 and runs flake8 to collect linting issues.
    Returns the formatted code plus any flake8 warnings.
    """
    # Format with autopep8
    formatted_code = autopep8.fix_code(code, options={"aggressive": 1})
    # Write to temp file for flake8
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".py", delete=False
    ) as tmp:
        tmp.write(formatted_code)
        tmp_path = tmp.name
    # Run flake8
    result = subprocess.run(
        ["flake8", tmp_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    os.unlink(tmp_path)
    issues = result.stdout.strip() or "No issues found."
    return f"{formatted_code}\n\n# Flake8 issues: \n{issues}"
