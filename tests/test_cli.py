"""Tests for PyLintPro CLI functionality."""

import tempfile
import os
import subprocess
import sys
from pathlib import Path


def test_cli_help():
    """Test CLI help functionality."""
    result = subprocess.run(
        [sys.executable, "lint.py", "--help"],
        cwd=Path(__file__).parent.parent,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "PyLintPro CLI" in result.stdout


def test_cli_basic_file():
    """Test CLI with a basic Python file."""
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                     delete=False) as f:
        f.write("""
def foo():
    x=1
    return x
""")
        test_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, "lint.py", test_file],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Processing:" in result.stdout
        assert "LINTING RESULTS" in result.stdout
    finally:
        os.unlink(test_file)
        # Clean up any generated fixed file
        fixed_file = test_file.replace('.py', '_fixed.py')
        if os.path.exists(fixed_file):
            os.unlink(fixed_file)
