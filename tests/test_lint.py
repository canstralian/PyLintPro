# tests/test_lint.py

import pytest
from src.lint import (
    lint_code,
    validate_python_syntax,
    enhanced_lint_code,
    basic_format_code
)


def test_validate_python_syntax_valid():
    """Test syntax validation with valid Python code."""
    code = "def hello():\n    print('world')\n    return 42"
    is_valid, error = validate_python_syntax(code)
    assert is_valid is True
    assert error is None


def test_validate_python_syntax_invalid():
    """Test syntax validation with invalid Python code."""
    code = "def hello(\n    print('world')"  # Missing closing parenthesis
    is_valid, error = validate_python_syntax(code)
    assert is_valid is False
    assert error is not None
    assert "Syntax Error" in error


def test_basic_format_code():
    """Test basic code formatting."""
    code = "def bad_function(x,y):\n    result=x+y\n    return result"
    formatted = basic_format_code(code)
    
    # Should add spaces around operators and after commas
    assert "x, y" in formatted
    assert "result = x + y" in formatted


def test_lint_code_empty():
    """Test lint_code with empty input."""
    result = lint_code("")
    assert result == "# No code provided"
    
    result = lint_code("   ")
    assert result == "# No code provided"


def test_lint_code_valid():
    """Test lint_code with valid Python code."""
    code = "def hello():\n    return 'world'\n"
    result = lint_code(code)
    
    # Should contain the original code and analysis
    assert "def hello():" in result
    assert "🔍 Linting Analysis:" in result


def test_enhanced_lint_code():
    """Test enhanced_lint_code functionality."""
    code = "def test():\n    pass\n"
    result = enhanced_lint_code(code)
    
    # Should contain the code and analysis
    assert "def test():" in result
    assert "🔍 Linting Analysis:" in result


def test_enhanced_lint_code_syntax_error():
    """Test enhanced_lint_code with syntax errors."""
    code = "def broken(\n    pass"  # Syntax error
    result = enhanced_lint_code(code)
    
    # Should indicate syntax error
    assert "❌" in result
    assert "Syntax Error" in result