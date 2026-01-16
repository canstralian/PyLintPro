"""Performance tests for PyLintPro optimization improvements."""

import time
from src.utils import parse_flake8_output


def test_parse_flake8_output_performance():
    """Test that parse_flake8_output handles large outputs efficiently."""
    # Create a large flake8 output
    large_output = "\n".join([
        f"file{i}.py:{i}:{i}: E501 line too long"
        for i in range(1, 1001)
    ])

    start = time.time()
    result = parse_flake8_output(large_output)
    elapsed = time.time() - start

    assert len(result) == 1000
    assert elapsed < 1.0  # Should complete in under 1 second
    assert result[0]['file'] == 'file1.py'
    assert result[0]['line'] == 1
    assert result[0]['code'] == 'E501'


def test_parse_flake8_output_with_errors():
    """Test that parse_flake8_output handles malformed lines gracefully."""
    output = """
file1.py:10:5: E501 line too long
malformed line without proper format
file2.py:20:10: W291 trailing whitespace
another bad line
"""
    result = parse_flake8_output(output)

    # Should only parse valid lines
    assert len(result) == 2
    assert result[0]['file'] == 'file1.py'
    assert result[1]['file'] == 'file2.py'


def test_parse_flake8_output_empty():
    """Test that parse_flake8_output handles empty output."""
    result = parse_flake8_output("")
    assert result == []


def test_parse_flake8_output_edge_cases():
    """Test edge cases in flake8 output parsing."""
    output = "path/to/file.py:1:1: E101 message with spaces"
    result = parse_flake8_output(output)

    assert len(result) == 1
    assert result[0]['file'] == 'path/to/file.py'
    assert result[0]['message'] == 'message with spaces'
