# tests/test_utils_new.py

import pytest
from src.utils import (
    safe_run, 
    parse_flake8_output, 
    format_issues_for_display,
    setup_logging
)


def test_safe_run():
    """Test the safe_run function with a simple command."""
    returncode, stdout, stderr = safe_run(["echo", "hello"])
    assert returncode == 0
    assert "hello" in stdout
    assert stderr == ""


def test_parse_flake8_output():
    """Test parsing of flake8 output."""
    sample_output = "test.py:1:1: E302 expected 2 blank lines, found 1"
    issues = parse_flake8_output(sample_output)
    
    assert len(issues) == 1
    assert issues[0]["file"] == "test.py"
    assert issues[0]["line"] == 1
    assert issues[0]["column"] == 1
    assert issues[0]["code"] == "E302"
    assert "expected 2 blank lines" in issues[0]["message"]


def test_format_issues_for_display():
    """Test formatting of issues for display."""
    issues = [
        {
            "file": "test.py",
            "line": 1,
            "column": 1,
            "code": "E302",
            "message": "expected 2 blank lines, found 1"
        }
    ]
    
    result = format_issues_for_display(issues)
    expected = "test.py:1:1 [E302] expected 2 blank lines, found 1"
    assert result == expected


def test_format_issues_empty():
    """Test formatting when no issues are found."""
    result = format_issues_for_display([])
    assert result == "No linting issues found."


def test_setup_logging():
    """Test that logging setup doesn't raise errors."""
    # This should not raise any exceptions
    setup_logging("test_logger", "DEBUG")
    setup_logging("test_logger2", "INFO")