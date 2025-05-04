import unittest
from app import lint_code

class TestLintCode(unittest.TestCase):
    """
    Unit tests for the lint_code function.
    """

    def test_lint_code_valid_code(self):
        """
        Test linting a valid code example.
        """
        code = "print( 'hello world' )"
        expected_output = "print('hello world')\n\n# Flake8 issues:\nNo issues found."
        self.assertEqual(lint_code(code), expected_output)

    def test_lint_code_invalid_code(self):
        """
        Test linting an invalid code example.
        """
        code = "print( 'hello world' )\nprint( 'hello again' )"
        result = lint_code(code)
        self.assertIn("print('hello world')\nprint('hello again')\n", result)
        self.assertIn("# Flake8 issues:\n", result)

    def test_lint_code_empty_code(self):
        """
        Test linting an empty code example.
        """
        code = ""
        expected_output = "\n\n# Flake8 issues:\nNo issues found."
        self.assertEqual(lint_code(code), expected_output)

if __name__ == "__main__":
    unittest.main()
