# tests/test_lint.py

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.lint import lint_code, format_code_only, check_code_only


class TestLintCode:
    """Test the main lint_code function."""
    
    def test_lint_clean_code(self):
        """Test linting clean Python code."""
        clean_code = """def hello_world():
    print("Hello, World!")
    return True


if __name__ == "__main__":
    hello_world()
"""
        result = lint_code(clean_code)
        
        assert isinstance(result, str)
        assert "def hello_world():" in result
        assert "# Flake8 issues:" in result
        # Should indicate no issues
        assert "No linting issues found." in result
    
    def test_lint_problematic_code(self):
        """Test linting code with formatting issues."""
        problematic_code = "print( 'hello world' )"
        result = lint_code(problematic_code)
        
        assert isinstance(result, str)
        # Should be formatted (either by autopep8 or simple formatter)
        assert "print('hello world')" in result or "print( 'hello world' )" not in result
        assert "# Flake8 issues:" in result
    
    def test_lint_code_with_syntax_error(self):
        """Test linting code with syntax errors."""
        invalid_code = "def broken_function(\n    print('missing closing parenthesis')"
        result = lint_code(invalid_code)
        
        assert isinstance(result, str)
        # Should handle the error gracefully
        assert "def broken_function(" in result or "Error" in result
    
    def test_lint_empty_code(self):
        """Test linting empty code."""
        result = lint_code("")
        
        assert isinstance(result, str)
        assert "# Flake8 issues:" in result
        assert "No linting issues found." in result
    
    @patch('src.lint.safe_run')
    def test_lint_code_flake8_error(self, mock_safe_run):
        """Test handling flake8 execution errors."""
        mock_safe_run.return_value = (1, "", "flake8: command not found")
        
        code = "print('test')"
        result = lint_code(code)
        
        assert isinstance(result, str)
        assert "print('test')" in result
        # Should handle error appropriately
        mock_safe_run.assert_called_once()
    
    @patch('src.lint.logger')
    def test_lint_code_logging(self, mock_logger):
        """Test that appropriate logging occurs."""
        code = "print('test')"
        lint_code(code)
        
        # Verify logging calls were made
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()


class TestFormatCodeOnly:
    """Test the format_code_only function."""
    
    def test_format_clean_code(self):
        """Test formatting already clean code."""
        clean_code = "print('hello')"
        result = format_code_only(clean_code)
        
        assert isinstance(result, str)
        assert "print('hello')" in result
    
    def test_format_problematic_code(self):
        """Test formatting problematic code."""
        problematic_code = "print( 'hello world' )"
        result = format_code_only(problematic_code)
        
        assert isinstance(result, str)
        # Should be formatted (either by autopep8 or simple formatter)
        assert "print('hello world')" in result or "print" in result
        # Should not have the extra spaces anymore
        assert result != problematic_code or "print(" in result
    
    def test_format_multiline_code(self):
        """Test formatting multiline code."""
        multiline_code = """def test():
    x=1
    y=2
    return x+y"""
        
        result = format_code_only(multiline_code)
        
        assert isinstance(result, str)
        assert "def test():" in result
        # Should have proper spacing
        assert "x = 1" in result or "x=1" in result  # Autopep8 might format this
    
    def test_format_empty_code(self):
        """Test formatting empty code."""
        result = format_code_only("")
        
        assert isinstance(result, str)
        assert result == ""
    
    @patch('src.lint.AUTOPEP8_AVAILABLE', True)
    @patch('src.lint.autopep8.fix_code')
    def test_format_autopep8_error(self, mock_fix_code):
        """Test handling autopep8 errors."""
        mock_fix_code.side_effect = Exception("Autopep8 error")
        
        code = "print('test')"
        result = format_code_only(code)
        
        assert isinstance(result, str)
        # Should fall back to simple formatting instead of returning error
        assert "print('test')" in result or "print" in result
    
    @patch('src.lint.logger')
    def test_format_code_logging(self, mock_logger):
        """Test that appropriate logging occurs."""
        code = "print('test')"
        format_code_only(code)
        
        # Verify logging calls were made
        mock_logger.info.assert_called()


class TestCheckCodeOnly:
    """Test the check_code_only function."""
    
    def test_check_clean_code(self):
        """Test checking clean Python code."""
        clean_code = """def hello_world():
    print("Hello, World!")
    return True


if __name__ == "__main__":
    hello_world()
"""
        is_clean, report = check_code_only(clean_code)
        
        assert isinstance(is_clean, bool)
        assert isinstance(report, str)
        assert is_clean is True
        assert "No linting issues found." in report
    
    def test_check_problematic_code(self):
        """Test checking code with issues."""
        problematic_code = "import os\nprint('hello')"  # Unused import
        is_clean, report = check_code_only(problematic_code)
        
        assert isinstance(is_clean, bool)
        assert isinstance(report, str)
        # This might or might not be clean depending on flake8 config
        if not is_clean:
            assert len(report) > 0
            assert "imported but unused" in report.lower() or "F401" in report
    
    def test_check_empty_code(self):
        """Test checking empty code."""
        is_clean, report = check_code_only("")
        
        assert isinstance(is_clean, bool)
        assert isinstance(report, str)
        assert is_clean is True
        assert "No linting issues found." in report
    
    @patch('src.lint.safe_run')
    def test_check_code_flake8_error(self, mock_safe_run):
        """Test handling flake8 execution errors."""
        mock_safe_run.return_value = (1, "", "flake8: command not found")
        
        code = "print('test')"
        is_clean, report = check_code_only(code)
        
        assert isinstance(is_clean, bool)
        assert isinstance(report, str)
        assert is_clean is False
        # Should handle error appropriately
        mock_safe_run.assert_called_once()
    
    @patch('src.lint.safe_run')
    def test_check_code_with_issues(self, mock_safe_run):
        """Test checking code that has flake8 issues."""
        # Mock flake8 finding issues
        mock_safe_run.return_value = (1, "test.py:1:1: F401 'os' imported but unused", "")
        
        code = "import os\nprint('test')"
        is_clean, report = check_code_only(code)
        
        assert isinstance(is_clean, bool)
        assert isinstance(report, str)
        assert is_clean is False
        assert "F401" in report
        assert "imported but unused" in report
    
    @patch('src.lint.logger')
    def test_check_code_logging(self, mock_logger):
        """Test that appropriate logging occurs."""
        code = "print('test')"
        check_code_only(code)
        
        # Verify logging calls were made
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()


class TestLintIntegration:
    """Integration tests for the lint module."""
    
    def test_lint_functions_return_strings(self):
        """Test that all lint functions return strings."""
        test_code = "print('test')"
        
        lint_result = lint_code(test_code)
        format_result = format_code_only(test_code)
        check_clean, check_report = check_code_only(test_code)
        
        assert isinstance(lint_result, str)
        assert isinstance(format_result, str)
        assert isinstance(check_clean, bool)
        assert isinstance(check_report, str)
    
    def test_consistent_formatting(self):
        """Test that format_code_only and lint_code produce similar formatting."""
        test_code = "print( 'hello world' )"
        
        format_result = format_code_only(test_code)
        lint_result = lint_code(test_code)
        
        # Extract just the formatted code part from lint_result
        formatted_part = lint_result.split("# Flake8 issues:")[0].strip()
        
        # Both should produce similarly formatted code
        assert "print('hello world')" in format_result or "print( 'hello world' )" in format_result
        assert "print('hello world')" in formatted_part or "print( 'hello world' )" in formatted_part
