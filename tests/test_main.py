import unittest
from src.main import main

class TestMainFunction(unittest.TestCase):
    """
    Unit tests for the main function in src/main.py.
    """

    def test_main_function(self):
        """
        Test the main function to ensure it runs without errors.
        """
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
