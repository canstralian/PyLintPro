# PyLintPro

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Flake8](https://img.shields.io/badge/Flake8-%E2%9C%94-green.svg)
![CI Status](https://img.shields.io/github/workflow/status/your-username/PyLintPro/CI)
![Issues](https://img.shields.io/github/issues/your-username/PyLintPro)

PyLintPro is a Gradio-based web application designed to help developers improve Python code by making it adhere to [Flake8](https://flake8.pycqa.org/) and [PEP 8](https://pep8.org/) standards. Simply paste your code or upload a `.py` file, and PyLintPro will return a linted version along with a detailed report of fixes. Whether you're working on personal projects or professional codebases, PyLintPro streamlines the process of cleaning and optimizing your Python code.

## Features

- **Code Linting**: Checks Python code against Flake8 rules to identify common issues such as style violations, potential bugs, and complexity problems.
- **PEP 8 Compliance**: Ensures your code follows the PEP 8 style guide, improving readability and maintainability.
- **File Upload Support**: Upload `.py` files and get the linted code and report back.
- **Real-time Linting**: Paste code into the textbox for immediate feedback and a fixed version of your code.
- **Customizable Linting Rules**: Choose which Flake8 rules to apply by selecting from a dropdown menu.
- **Code Fixing with autopep8**: Automatically fix common style issues in your Python code using the `autopep8` tool.
- **Linting Reports**: Get a detailed report on your code’s style issues, including statistics on what was fixed and what still needs attention.
- **Minimalist, User-friendly Interface**: Powered by Gradio, with a clean and intuitive interface that’s easy to navigate.

## Getting Started

### Prerequisites

Before using PyLintPro, ensure you have the following installed:

- **Python 3.9+**: PyLintPro works with Python 3.9 and above.
- **Flake8**: A Python tool for enforcing PEP 8 coding style.
- **autopep8**: A tool to automatically fix PEP 8 issues in Python code.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/PyLintPro.git
    cd PyLintPro
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app locally:

    ```bash
    python app.py
    ```

4. Navigate to the local address in your browser (e.g., `http://127.0.0.1:7860`) to start linting your Python code.

### Usage

1. **Paste Code**: In the text input box, paste your Python code.
2. **Upload File**: Click the "Upload Code File" button to select a `.py` file from your computer. The app will process the file and display the linted code.
3. **Select Linting Rules**: Choose which Flake8 rules to apply by selecting from the provided list of common rules.
4. **Submit**: Click the "Submit" button to run the linting process. The app will display:
    - The **linted code** with improvements.
    - A **linting report** showing the issues identified and fixed.

### Example

Here's an example of how to use the app:

1. Paste this Python code into the input box:
    ```python
    import os
    import sys
    def main():
    print('Hello World')
    ```

2. After clicking "Submit", the app will return the following linted version:
    ```python
    import os
    import sys

    def main():
        print('Hello World')
    ```

   **Linting Report**:
    - `E701`: Multiple statements on one line.
    - `W292`: No newline at end of file.

### Options & Customization

- **Choose Linting Rules**: Select multiple Flake8 rules to customize which issues should be flagged. You can choose to ignore specific warnings such as line length issues (`E501`) or unused imports (`F401`).
- **File Upload Support**: If you have an existing `.py` file, simply upload it, and the app will automatically lint the code.

### Advanced Configuration

PyLintPro also supports several advanced configurations:

- **Ignore Specific Rules**: You can specify which Flake8 rules to ignore when running the linting process.
- **Custom PEP 8 Guidelines**: If your project requires custom coding standards, you can configure PyLintPro to enforce those standards by modifying the `flake8` configuration file.

## Contributing

We welcome contributions to PyLintPro! If you'd like to contribute, please fork the repository and submit a pull request. Here are some ways you can help:

- Report bugs or issues.
- Suggest new features or enhancements.
- Submit code fixes or improvements.

### How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

Please ensure that your code adheres to the following:

- Follow PEP 8 and Flake8 standards.
- Ensure that tests pass and linting is successful.

## License

PyLintPro is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Gradio](https://gradio.app/): Used for building the user-friendly interface.
- [Flake8](https://flake8.pycqa.org/): Linting tool used to check code against PEP 8.
- [autopep8](https://github.com/hhatto/autopep8): Used to auto-correct PEP 8 violations.

---

### Example Code Snippet for Reference

Here’s an example Python code snippet that can be used with PyLintPro:

```python
import sys

def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()

Known Issues
   •   File Upload Limit: Currently, the maximum file size for uploads is 10 MB.
   •   Performance on Large Files: The app may take longer to process large files or files with many lines of code.

Contact

For more information, contact us at support@pylintpro.com.

Footer

PyLintPro is powered by Flake8 and autopep8, designed to enhance Python code quality with minimal effort.

### Explanation of Badges:

1. **License Badge**: Shows the license type for the project (MIT License).
2. **Python Version Badge**: Indicates that PyLintPro supports Python 3.9 and above.
3. **Flake8 Badge**: Displays that PyLintPro integrates Flake8 for linting and is Flake8-compliant.
4. **CI Status Badge**: Indicates the status of the continuous integration pipeline for the repository (e.g., passing or failing).
5. **Issues Badge**: Displays the number of open issues in the repository, helping users track bugs or requests.

