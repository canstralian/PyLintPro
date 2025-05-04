import unittest
from scripts.preprocess import preprocess_example

class TestPreprocessExample(unittest.TestCase):
    """
    Unit tests for the preprocess_example function.
    """

    def test_preprocess_example_valid_code(self):
        """
        Test preprocessing a valid code example.
        """
        example = {"code": "print( 'hello world' )"}
        result = preprocess_example(example)
        self.assertIn("formatted_code", result)
        self.assertIn("issues", result)
        self.assertEqual(result["formatted_code"], "print('hello world')\n")
        self.assertEqual(result["issues"], [])

    def test_preprocess_example_invalid_code(self):
        """
        Test preprocessing an invalid code example.
        """
        example = {"code": "print( 'hello world' )\nprint( 'hello again' )"}
        result = preprocess_example(example)
        self.assertIn("formatted_code", result)
        self.assertIn("issues", result)
        self.assertEqual(result["formatted_code"], "print('hello world')\nprint('hello again')\n")
        self.assertNotEqual(result["issues"], [])

    def test_preprocess_example_empty_code(self):
        """
        Test preprocessing an empty code example.
        """
        example = {"code": ""}
        result = preprocess_example(example)
        self.assertIn("formatted_code", result)
        self.assertIn("issues", result)
        self.assertEqual(result["formatted_code"], "")
        self.assertEqual(result["issues"], [])

if __name__ == "__main__":
    unittest.main()
