# src/lint.py

import tempfile
import os
import re
from typing import Tuple, Optional
from src.utils import safe_run, parse_flake8_output, format_issues_for_display


def basic_format_code(code: str) -> str:
    """
    Apply basic Python formatting improvements.

    Args:
        code: Python source code to format

    Returns:
        Formatted Python code
    """
    if not code or not code.strip():
        return code

    lines = code.split('\n')
    formatted_lines = []

    for line in lines:
        # Basic formatting rules
        # Add space after commas (but not in strings)
        if (not line.strip().startswith('#') and
                not line.strip().startswith('"""')):
            # Simple comma spacing fix
            line = re.sub(r',(\S)', r', \1', line)
            # Simple operator spacing fix
            line = re.sub(r'(\w)=(\w)', r'\1 = \2', line)
            line = re.sub(r'(\w)\+(\w)', r'\1 + \2', line)
            line = re.sub(r'(\w)-(\w)', r'\1 - \2', line)

        formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def lint_code(code: str) -> str:
    """
    Runs flake8 to collect linting issues on Python code.

    Args:
        code: The Python source code to lint and format

    Returns:
        Original code with linting issues appended as comments
    """
    if not code or not code.strip():
        return "# No code provided"

    try:
        # Write to temp file for flake8 analysis
        with tempfile.NamedTemporaryFile(
            mode="w+",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            # Run flake8 with custom configuration
            returncode, stdout, stderr = safe_run([
                "flake8",
                tmp_path,
                "--max-line-length=88",
                "--ignore=E203,W503",  # Compatible with Black
                "--statistics"
            ])

            # Parse flake8 output
            if stdout.strip():
                issues = parse_flake8_output(stdout)
                issues_text = format_issues_for_display(issues)
            else:
                issues_text = "✅ No linting issues found!"

        except Exception as e:
            issues_text = f"⚠️ Linting analysis failed: {str(e)}"

        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        # Return original code with issues
        analysis_header = "# 🔍 Linting Analysis:"
        analysis_text = f"{code}\n\n{analysis_header}\n# {issues_text}"
        return analysis_text

    except Exception as e:
        return f"# ❌ Error processing code: {str(e)}\n\n{code}"


def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Python syntax without executing the code.

    Args:
        code: Python source code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        compile(code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
        return False, error_msg
    except Exception as e:
        return False, f"Compilation error: {str(e)}"


def enhanced_lint_code(code: str) -> str:
    """
    Enhanced version of lint_code with syntax validation and basic formatting.

    Args:
        code: The Python source code to lint and format

    Returns:
        Enhanced formatted code with comprehensive analysis
    """
    if not code or not code.strip():
        return "# No code provided for analysis"

    # First validate syntax
    is_valid, syntax_error = validate_python_syntax(code)
    if not is_valid:
        return f"# ❌ {syntax_error}\n\n{code}"

    # Apply basic formatting
    formatted_code = basic_format_code(code)

    # Run linting on formatted code
    result = lint_code(formatted_code)

    # Add syntax validation confirmation
    if "✅ No linting issues found!" in result:
        result = result.replace(
            "✅ No linting issues found!",
            "✅ Code is syntactically valid and follows PEP 8 standards!"
        )

    return result
