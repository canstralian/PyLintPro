import unittest
from fastapi.testclient import TestClient
from scripts.run_backend import app, LintRequest

class TestRunBackend(unittest.TestCase):
    """
    Unit tests for the lint_endpoint function in scripts/run_backend.py.
    """

    def setUp(self):
        """
        Set up the test client.
        """
        self.client = TestClient(app)

    def test_lint_endpoint_valid_code(self):
        """
        Test linting a valid code example.
        """
        request_data = LintRequest(code="print( 'hello world' )")
        response = self.client.post("/lint", json=request_data.dict())
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("formatted_code", response_data)
        self.assertIn("issues", response_data)
        self.assertEqual(response_data["formatted_code"], "print('hello world')\n")
        self.assertEqual(response_data["issues"], [])

    def test_lint_endpoint_invalid_code(self):
        """
        Test linting an invalid code example.
        """
        request_data = LintRequest(code="print( 'hello world' )\nprint( 'hello again' )")
        response = self.client.post("/lint", json=request_data.dict())
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("formatted_code", response_data)
        self.assertIn("issues", response_data)
        self.assertEqual(response_data["formatted_code"], "print('hello world')\nprint('hello again')\n")
        self.assertNotEqual(response_data["issues"], [])

    def test_lint_endpoint_empty_code(self):
        """
        Test linting an empty code example.
        """
        request_data = LintRequest(code="")
        response = self.client.post("/lint", json=request_data.dict())
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("formatted_code", response_data)
        self.assertIn("issues", response_data)
        self.assertEqual(response_data["formatted_code"], "")
        self.assertEqual(response_data["issues"], [])

if __name__ == "__main__":
    unittest.main()
