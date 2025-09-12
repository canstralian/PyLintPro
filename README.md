# 🔧 PyLintPro

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flake8](https://img.shields.io/badge/Flake8-6.0.0-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-5.45.0-purple.svg)

---

**PyLintPro** is an **AI-enhanced Python code quality tool** built with Gradio that helps developers improve their Python code to meet **PEP 8 and Flake8 standards**.

Think of it as your **intelligent code quality assistant** — combining **automated linting, basic formatting, and real-time feedback** in an easy-to-use web interface.

---

## ✨ Features

- 🔍 **Advanced Code Analysis**
  - Real-time Flake8 linting with detailed error reporting
  - Python syntax validation before processing
  - Comprehensive error categorization and explanations

- 🎨 **Smart Code Formatting**
  - Basic Python code formatting (spacing, operators)
  - PEP 8 compliance checking
  - Line length and style validation

- 🌐 **Interactive Web Interface**
  - Clean Gradio-based UI with side-by-side code editors
  - Pre-loaded examples for quick testing
  - Real-time linting feedback with emojis and formatting

- ⚙️ **Robust Architecture**
  - Modular codebase with proper separation of concerns
  - Comprehensive error handling and logging
  - Type hints and documentation throughout
  - Full test coverage with pytest

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/canstralian/PyLintPro.git
cd PyLintPro

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://127.0.0.1:7860`

---

## 🛠️ Usage

### Web Interface

1. **Start the application**: `python app.py`
2. **Open your browser** to `http://127.0.0.1:7860`
3. **Paste your Python code** in the left editor
4. **Click "Lint Code"** to get formatted code and analysis
5. **Review the results** in the right editor with detailed feedback

### Modular Usage

You can also use PyLintPro as a Python module:

```python
from src.lint import enhanced_lint_code

code = """
def bad_function( x,y ):
    result=x+y
    return result
"""

result = enhanced_lint_code(code)
print(result)
```

### CLI Usage

```bash
# Run with PYTHONPATH
PYTHONPATH=. python src/main.py
```

---

## 📊 Code Quality Features

### Syntax Validation
- ✅ Validates Python syntax before processing
- ❌ Reports syntax errors with line numbers and descriptions
- 🔧 Prevents processing of invalid code

### Linting Analysis
- **Flake8 Integration**: Uses Flake8 6.0.0 for comprehensive code analysis
- **PEP 8 Compliance**: Checks for Python style guide violations
- **Detailed Reports**: Line-by-line issue reporting with error codes
- **Smart Filtering**: Ignores formatting conflicts (E203, W503)

### Basic Formatting
- **Operator Spacing**: Adds spaces around `=`, `+`, `-` operators
- **Comma Spacing**: Fixes spacing after commas in function parameters
- **Non-destructive**: Preserves original code structure and comments

---

## 🏗️ Architecture

```
PyLintPro/
├── src/
│   ├── __init__.py      # Package initialization and exports
│   ├── config.py        # Configuration and constants
│   ├── lint.py          # Core linting and formatting logic
│   ├── main.py          # Modular Gradio application
│   └── utils.py         # Utility functions and helpers
├── tests/
│   ├── test_lint.py     # Tests for linting functionality
│   └── test_utils_new.py # Tests for utility functions
├── app.py               # Standalone Gradio application
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project configuration
```

### Key Components

- **`src/lint.py`**: Core linting engine with syntax validation and formatting
- **`src/utils.py`**: Utility functions for command execution and output parsing
- **`src/config.py`**: Centralized configuration and theming
- **`app.py`**: Standalone web application
- **`src/main.py`**: Modular web application

---

## 🧪 Testing

PyLintPro includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest

# Run specific test files
python -m pytest tests/test_lint.py -v
python -m pytest tests/test_utils_new.py -v

# Run with verbose output
python -m pytest -v
```

**Test Coverage**: 12 tests covering:
- Syntax validation functionality
- Code formatting operations
- Linting engine integration
- Utility function behavior
- Error handling scenarios

---

## ⚡ Performance

- **Fast Processing**: Optimized for quick feedback on code changes
- **Memory Efficient**: Uses temporary files for safe code analysis
- **Error Resilient**: Comprehensive error handling prevents crashes
- **Scalable**: Modular design supports easy feature additions

---

## 🛠️ Development

### Code Quality Standards

PyLintPro follows its own standards:
- **PEP 8 Compliance**: All code follows Python style guidelines
- **Type Hints**: Full type annotation for better IDE support
- **Documentation**: Comprehensive docstrings for all functions
- **Testing**: High test coverage with pytest

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow coding standards**: Use Flake8 and format with the project style
4. **Add tests**: Ensure new features are tested
5. **Submit a Pull Request**

---

## 📦 Dependencies

- **Core**: `gradio>=5.45.0`, `flake8==6.0.0`
- **Development**: `pytest>=8.4.0`
- **Optional**: `autopep8==2.0.2` (for advanced formatting)

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Code Style**: Follow PEP 8 and use type hints
2. **Testing**: Add tests for new functionality
3. **Documentation**: Update docs for user-facing changes
4. **Git**: Use clear commit messages and proper branching

---

## 📄 License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **Gradio**: For the excellent web interface framework
- **Flake8**: For comprehensive Python linting capabilities
- **Python Community**: For the PEP 8 style guide and best practices

---

## 📫 Support

- **GitHub Issues**: [Submit a Bug Report](https://github.com/canstralian/PyLintPro/issues)
- **Documentation**: Check the code comments and tests for examples
- **Community**: Share your experience and improvements

---

🔧 **PyLintPro** — Your intelligent companion for clean, professional Python code.

---