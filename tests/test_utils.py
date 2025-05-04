import unittest
from unittest.mock import patch, MagicMock
from src.utils import safe_run, parse_flake8_output, format_issues_for_display

class TestUtils(unittest.TestCase):
    """
    Unit tests for utility functions in src/utils.py.
    """

    @patch("subprocess.run")
    def test_safe_run(self, mock_run):
        """
        Test safe_run function.
        """
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = "error"
        mock_run.return_value = mock_result

        returncode, stdout, stderr = safe_run(["echo", "hello"])
        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, "output")
        self.assertEqual(stderr, "error")

    def test_parse_flake8_output(self):
        """
        Test parse_flake8_output function.
        """
        output = "file.py:1:1: E999 SyntaxError: invalid syntax\nfile.py:2:1: W292 no newline at end of file"
        expected_issues = [
            {
                "file": "file.py",
                "line": 1,
                "column": 1,
                "code": "E999",
                "message": "SyntaxError: invalid syntax"
            },
            {
                "file": "file.py",
                "line": 2,
                "column": 1,
                "code": "W292",
                "message": "no newline at end of file"
            }
        ]
        issues = parse_flake8_output(output)
        self.assertEqual(issues, expected_issues)

    def test_format_issues_for_display(self):
        """
        Test format_issues_for_display function.
        """
        issues = [
            {
                "file": "file.py",
                "line": 1,
                "column": 1,
                "code": "E999",
                "message": "SyntaxError: invalid syntax"
            },
            {
                "file": "file.py",
                "line": 2,
                "column": 1,
                "code": "W292",
                "message": "no newline at end of file"
            }
        ]
        expected_output = (
            "file.py:1:1 [E999] SyntaxError: invalid syntax\n"
            "file.py:2:1 [W292] no newline at end of file"
        )
        formatted_output = format_issues_for_display(issues)
        self.assertEqual(formatted_output, expected_output)

if __name__ == "__main__":
    unittest.main()
