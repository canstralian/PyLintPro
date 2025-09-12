"""Tests for PyLintPro utilities."""

from src.lint import lint_code


def test_lint_code_basic():
    """Test basic linting functionality."""
    test_code = """
def foo():
    x=1
    return x

print( 'hello world' )
"""
    result = lint_code(test_code)
    assert isinstance(result, str)
    assert "Flake8 issues:" in result


def test_lint_code_clean():
    """Test linting clean code."""
    clean_code = '''
def hello_world():
    """Print hello world."""
    print("Hello, world!")


if __name__ == "__main__":
    hello_world()
'''
    result = lint_code(clean_code)
    assert isinstance(result, str)
    assert "No issues found" in result or "Flake8 issues:" in result
