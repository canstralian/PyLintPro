import unittest
import pandas as pd
from data.data_preprocessing import load_data

class TestLoadData(unittest.TestCase):
    """
    Unit tests for the load_data function.
    """

    def test_load_data_valid_file(self):
        """
        Test loading data from a valid CSV file.
        """
        df = load_data("tests/test_data/valid_data.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 2))  # Assuming the test CSV has 3 rows and 2 columns

    def test_load_data_invalid_file(self):
        """
        Test loading data from an invalid file path.
        """
        with self.assertRaises(FileNotFoundError):
            load_data("tests/test_data/non_existent_file.csv")

    def test_load_data_empty_file(self):
        """
        Test loading data from an empty CSV file.
        """
        df = load_data("tests/test_data/empty_data.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

if __name__ == "__main__":
    unittest.main()
