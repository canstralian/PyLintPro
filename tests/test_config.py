# tests/test_config.py

import pytest
from pathlib import Path

from src.config import (
    BASE_DIR,
    FLAKE8_CONFIG,
    PYPROJECT_TOML,
    DEFAULT_MAX_LINE_LENGTH,
    DEFAULT_IGNORE_RULES,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    GRADIO_THEME,
    GRADIO_CSS,
)


class TestConfigConstants:
    """Test configuration constants and values."""
    
    def test_base_dir_exists(self):
        """Test that BASE_DIR points to an existing directory."""
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()
    
    def test_base_dir_is_absolute(self):
        """Test that BASE_DIR is an absolute path."""
        assert BASE_DIR.is_absolute()
    
    def test_config_file_paths(self):
        """Test configuration file paths are properly constructed."""
        assert FLAKE8_CONFIG == BASE_DIR / ".flake8"
        assert PYPROJECT_TOML == BASE_DIR / "pyproject.toml"
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert PYPROJECT_TOML.exists()
        assert PYPROJECT_TOML.is_file()
    
    def test_default_linting_settings(self):
        """Test default linting configuration values."""
        assert DEFAULT_MAX_LINE_LENGTH == 88
        assert isinstance(DEFAULT_IGNORE_RULES, list)
        assert "E203" in DEFAULT_IGNORE_RULES
        assert "W503" in DEFAULT_IGNORE_RULES
    
    def test_app_metadata(self):
        """Test application metadata constants."""
        assert isinstance(APP_NAME, str)
        assert APP_NAME == "PyLintPro"
        
        assert isinstance(APP_VERSION, str)
        assert APP_VERSION == "1.0.0"
        
        assert isinstance(APP_DESCRIPTION, str)
        assert len(APP_DESCRIPTION) > 0
        assert "Gradio" in APP_DESCRIPTION
        assert "Flake8" in APP_DESCRIPTION
    
    def test_gradio_settings(self):
        """Test Gradio interface configuration."""
        assert isinstance(GRADIO_THEME, str)
        assert GRADIO_THEME == "default"
        
        assert isinstance(GRADIO_CSS, str)
        assert "gradio-container" in GRADIO_CSS
        assert "padding" in GRADIO_CSS


class TestConfigTypes:
    """Test that configuration values have correct types."""
    
    def test_path_types(self):
        """Test that path configurations are Path objects."""
        assert isinstance(BASE_DIR, Path)
        assert isinstance(FLAKE8_CONFIG, Path)
        assert isinstance(PYPROJECT_TOML, Path)
    
    def test_string_types(self):
        """Test that string configurations are strings."""
        assert isinstance(APP_NAME, str)
        assert isinstance(APP_VERSION, str)
        assert isinstance(APP_DESCRIPTION, str)
        assert isinstance(GRADIO_THEME, str)
        assert isinstance(GRADIO_CSS, str)
    
    def test_numeric_types(self):
        """Test that numeric configurations are correct types."""
        assert isinstance(DEFAULT_MAX_LINE_LENGTH, int)
        assert DEFAULT_MAX_LINE_LENGTH > 0
    
    def test_list_types(self):
        """Test that list configurations are lists."""
        assert isinstance(DEFAULT_IGNORE_RULES, list)
        assert len(DEFAULT_IGNORE_RULES) > 0
        assert all(isinstance(rule, str) for rule in DEFAULT_IGNORE_RULES)


class TestConfigValues:
    """Test specific configuration values."""
    
    def test_base_dir_structure(self):
        """Test that BASE_DIR contains expected project structure."""
        # Check for essential project directories/files
        assert (BASE_DIR / "src").exists()
        assert (BASE_DIR / "tests").exists()
        assert (BASE_DIR / "README.md").exists()
        assert (BASE_DIR / "pyproject.toml").exists()
    
    def test_ignore_rules_format(self):
        """Test that ignore rules follow expected format."""
        for rule in DEFAULT_IGNORE_RULES:
            # Rules should be alphanumeric codes
            assert rule.replace("-", "").isalnum()
            assert len(rule) >= 3  # Minimum reasonable rule length
    
    def test_version_format(self):
        """Test that version follows semantic versioning pattern."""
        version_parts = APP_VERSION.split(".")
        assert len(version_parts) == 3
        assert all(part.isdigit() for part in version_parts)
    
    def test_gradio_css_validity(self):
        """Test that Gradio CSS is valid CSS-like syntax."""
        # Basic CSS syntax check
        assert "{" in GRADIO_CSS
        assert "}" in GRADIO_CSS
        assert ":" in GRADIO_CSS
        assert ";" in GRADIO_CSS
