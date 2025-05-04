import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestEndToEnd(unittest.TestCase):
    """
    End-to-end tests to simulate real user interactions with the application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Selenium WebDriver.
        """
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.get("http://localhost:7860")  # Assuming the Gradio app is running locally on port 7860

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the Selenium WebDriver.
        """
        cls.driver.quit()

    def test_lint_code(self):
        """
        Test the linting functionality of the application.
        """
        code_input = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Your Code']")
        code_input.send_keys("print( 'hello world' )")
        lint_button = self.driver.find_element(By.XPATH, "//button[text()='Lint Code']")
        lint_button.click()
        time.sleep(2)  # Wait for the linting process to complete
        code_output = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Linted Code']")
        self.assertIn("print('hello world')", code_output.get_attribute("value"))

    def test_example_snippets(self):
        """
        Test the example snippets functionality.
        """
        example_button = self.driver.find_element(By.XPATH, "//button[text()='Try These Snippets']")
        example_button.click()
        time.sleep(1)  # Wait for the example snippet to be loaded
        code_input = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Your Code']")
        self.assertIn("print( 'hello world' )", code_input.get_attribute("value"))

if __name__ == "__main__":
    unittest.main()
