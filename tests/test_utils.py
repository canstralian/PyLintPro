# tests/test_utils.py

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, mock_open
import yaml
import logging

from src.utils import (
    safe_run,
    parse_flake8_output,
    format_issues_for_display,
    load_examples,
    load_yaml_config,
    setup_logging
)


class TestSafeRun:
    """Test the safe_run utility function."""
    
    def test_safe_run_success(self):
        """Test safe_run with a successful command."""
        returncode, stdout, stderr = safe_run(["echo", "hello"])
        assert returncode == 0
        assert "hello" in stdout
        assert stderr == ""
    
    def test_safe_run_failure(self):
        """Test safe_run with a failing command."""
        returncode, stdout, stderr = safe_run(["ls", "/nonexistent"])
        assert returncode != 0
        assert stdout == ""
        assert len(stderr) > 0
    
    def test_safe_run_with_cwd(self):
        """Test safe_run with a specific working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            returncode, stdout, stderr = safe_run(["pwd"], cwd=Path(tmpdir))
            assert returncode == 0
            assert tmpdir in stdout
    
    @patch('subprocess.run')
    def test_safe_run_timeout(self, mock_run):
        """Test safe_run with timeout parameter."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "output"
        mock_run.return_value.stderr = ""
        
        safe_run(["echo", "test"], timeout=10)
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert kwargs['timeout'] == 10
        assert kwargs['shell'] is False


class TestParseFlake8Output:
    """Test the flake8 output parser."""
    
    def test_parse_empty_output(self):
        """Test parsing empty flake8 output."""
        result = parse_flake8_output("")
        assert result == []
    
    def test_parse_single_issue(self):
        """Test parsing single flake8 issue."""
        output = "test.py:1:5: E203 whitespace before ':'"
        result = parse_flake8_output(output)
        
        assert len(result) == 1
        assert result[0] == {
            "file": "test.py",
            "line": 1,
            "column": 5,
            "code": "E203",
            "message": "whitespace before ':'"
        }
    
    def test_parse_multiple_issues(self):
        """Test parsing multiple flake8 issues."""
        output = """test.py:1:5: E203 whitespace before ':'
test.py:2:10: F401 'os' imported but unused
another.py:5:1: E302 expected 2 blank lines, found 1"""
        
        result = parse_flake8_output(output)
        assert len(result) == 3
        
        # Check first issue
        assert result[0]["file"] == "test.py"
        assert result[0]["line"] == 1
        assert result[0]["code"] == "E203"
        
        # Check second issue
        assert result[1]["file"] == "test.py"
        assert result[1]["line"] == 2
        assert result[1]["code"] == "F401"
        
        # Check third issue
        assert result[2]["file"] == "another.py"
        assert result[2]["line"] == 5
        assert result[2]["code"] == "E302"
    
    def test_parse_malformed_output(self):
        """Test parsing malformed flake8 output."""
        output = "invalid line format"
        result = parse_flake8_output(output)
        assert result == []


class TestFormatIssuesForDisplay:
    """Test the issue formatting function."""
    
    def test_format_empty_issues(self):
        """Test formatting empty issues list."""
        result = format_issues_for_display([])
        assert result == "No linting issues found."
    
    def test_format_single_issue(self):
        """Test formatting single issue."""
        issues = [{
            "file": "test.py",
            "line": 1,
            "column": 5,
            "code": "E203",
            "message": "whitespace before ':'"
        }]
        
        result = format_issues_for_display(issues)
        expected = "test.py:1:5 [E203] whitespace before ':'"
        assert result == expected
    
    def test_format_multiple_issues(self):
        """Test formatting multiple issues."""
        issues = [
            {
                "file": "test.py",
                "line": 1,
                "column": 5,
                "code": "E203",
                "message": "whitespace before ':'"
            },
            {
                "file": "test.py",
                "line": 2,
                "column": 10,
                "code": "F401",
                "message": "'os' imported but unused"
            }
        ]
        
        result = format_issues_for_display(issues)
        lines = result.split('\n')
        assert len(lines) == 2
        assert "test.py:1:5 [E203] whitespace before ':'" in lines[0]
        assert "test.py:2:10 [F401] 'os' imported but unused" in lines[1]


class TestLoadExamples:
    """Test the example loading function."""
    
    def test_load_examples_existing_directory(self):
        """Test loading examples from an existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            examples_dir = Path(tmpdir)
            
            # Create test Python files
            (examples_dir / "example1.py").write_text("print('hello')")
            (examples_dir / "example2.py").write_text("def test():\n    pass")
            
            result = load_examples(examples_dir)
            assert len(result) == 2
            assert "print('hello')" in result
            assert "def test():\n    pass" in result
    
    def test_load_examples_nonexistent_directory(self):
        """Test loading examples from a non-existent directory."""
        nonexistent_dir = Path("/tmp/nonexistent_dir_12345")
        result = load_examples(nonexistent_dir)
        assert result == []
    
    def test_load_examples_empty_directory(self):
        """Test loading examples from an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            examples_dir = Path(tmpdir)
            result = load_examples(examples_dir)
            assert result == []
    
    def test_load_examples_non_python_files(self):
        """Test loading examples with non-Python files present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            examples_dir = Path(tmpdir)
            
            # Create Python and non-Python files
            (examples_dir / "example.py").write_text("print('test')")
            (examples_dir / "readme.txt").write_text("not python")
            (examples_dir / "config.json").write_text("{}")
            
            result = load_examples(examples_dir)
            assert len(result) == 1
            assert "print('test')" in result[0]


class TestLoadYamlConfig:
    """Test the YAML config loading function."""
    
    def test_load_valid_yaml(self):
        """Test loading valid YAML configuration."""
        yaml_content = """
key1: value1
key2:
  nested: value2
list_key:
  - item1
  - item2
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp.write(yaml_content)
            tmp_path = Path(tmp.name)
        
        try:
            result = load_yaml_config(tmp_path)
            assert result["key1"] == "value1"
            assert result["key2"]["nested"] == "value2"
            assert result["list_key"] == ["item1", "item2"]
        finally:
            tmp_path.unlink()
    
    def test_load_empty_yaml(self):
        """Test loading empty YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp.write("")
            tmp_path = Path(tmp.name)
        
        try:
            result = load_yaml_config(tmp_path)
            assert result is None
        finally:
            tmp_path.unlink()
    
    def test_load_invalid_yaml(self):
        """Test loading invalid YAML file."""
        invalid_yaml = "key: value\n  invalid: indentation"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp.write(invalid_yaml)
            tmp_path = Path(tmp.name)
        
        try:
            with pytest.raises(yaml.YAMLError):
                load_yaml_config(tmp_path)
        finally:
            tmp_path.unlink()


class TestSetupLogging:
    """Test the logging setup function."""
    
    def test_setup_logging_default(self):
        """Test setting up logging with default parameters."""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        setup_logging()
        
        # Check that logging is configured
        logger = logging.getLogger(__name__)
        assert logger.level <= logging.INFO
    
    def test_setup_logging_custom_level(self):
        """Test setting up logging with custom level."""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        setup_logging(level="DEBUG")
        
        # Check that debug level is set
        logger = logging.getLogger(__name__)
        assert logger.level <= logging.DEBUG
    
    def test_setup_logging_custom_name(self):
        """Test setting up logging with custom logger name."""
        test_name = "test.custom.logger"
        setup_logging(name=test_name)
        
        # This should not raise an exception
        logger = logging.getLogger(test_name)
        assert logger is not None
