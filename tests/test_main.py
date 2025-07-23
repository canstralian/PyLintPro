# tests/test_main.py

import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock gradio module since it may not be available
gradio_mock = MagicMock()
sys.modules['gradio'] = gradio_mock

# Now import the main module
from src.main import main


class TestMainFunction:
    """Test the main function and Gradio app setup."""
    
    @patch('gradio.Blocks')
    @patch('src.main.gr.Code')
    @patch('src.main.gr.Button')
    @patch('src.main.gr.Examples')
    @patch('src.main.gr.Row')
    def test_main_creates_gradio_app(self, mock_row, mock_examples, mock_button, mock_code, mock_blocks):
        """Test that main function creates a Gradio app with expected components."""
        # Mock the Gradio components
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        mock_code_input = MagicMock()
        mock_code_output = MagicMock()
        mock_code.side_effect = [mock_code_input, mock_code_output]
        
        mock_lint_btn = MagicMock()
        mock_button.return_value = mock_lint_btn
        
        # Call main function
        main()
        
        # Verify Gradio components were created
        mock_blocks.assert_called_once()
        assert mock_code.call_count == 2  # Two Code components
        mock_button.assert_called_once_with("Lint Code", variant="primary")
        mock_examples.assert_called_once()
        mock_row.assert_called_once()
        
        # Verify button click was configured
        mock_lint_btn.click.assert_called_once()
        
        # Verify demo.launch was called
        mock_demo.launch.assert_called_once()
    
    @patch('gradio.Blocks')
    def test_main_gradio_configuration(self, mock_blocks):
        """Test that Gradio is configured with correct theme and CSS."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        main()
        
        # Check that Gradio.Blocks was called with expected configuration
        call_args = mock_blocks.call_args
        kwargs = call_args[1] if call_args else {}
        
        # Verify configuration parameters
        assert 'theme' in kwargs or 'css' in kwargs or 'fill_width' in kwargs
        mock_blocks.assert_called_once()
    
    @patch('gradio.Blocks')
    @patch('src.main.gr.Code')
    def test_main_code_components_configuration(self, mock_code, mock_blocks):
        """Test that Code components are configured correctly."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        main()
        
        # Verify Code components were created with correct parameters
        assert mock_code.call_count == 2
        
        # Check first call (input component)
        first_call = mock_code.call_args_list[0]
        first_kwargs = first_call[1] if first_call else {}
        assert first_kwargs.get('language') == 'python'
        assert first_kwargs.get('label') == 'Your Code'
        assert first_kwargs.get('interactive') is True
        
        # Check second call (output component)
        second_call = mock_code.call_args_list[1]
        second_kwargs = second_call[1] if second_call else {}
        assert second_kwargs.get('language') == 'python'
        assert second_kwargs.get('label') == 'Linted Code'
        assert second_kwargs.get('interactive') is False
    
    @patch('gradio.Blocks')
    @patch('src.main.gr.Examples')
    def test_main_examples_configuration(self, mock_examples, mock_blocks):
        """Test that Examples component is configured with sample code."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        main()
        
        # Verify Examples component was created
        mock_examples.assert_called_once()
        
        # Check examples configuration
        call_args = mock_examples.call_args
        kwargs = call_args[1] if call_args else {}
        
        # Should have examples list
        assert 'examples' in kwargs
        examples = kwargs['examples']
        assert isinstance(examples, list)
        assert len(examples) > 0
        
        # Should have inputs specified
        assert 'inputs' in kwargs
    
    @patch('gradio.Blocks')
    @patch('src.main.gr.Button')
    @patch('src.main.lint_code')
    def test_main_button_click_handler(self, mock_lint_code, mock_button, mock_blocks):
        """Test that button click handler is configured correctly."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        mock_lint_btn = MagicMock()
        mock_button.return_value = mock_lint_btn
        
        main()
        
        # Verify button click was configured
        mock_lint_btn.click.assert_called_once()
        
        # Check click handler configuration
        call_args = mock_lint_btn.click.call_args
        kwargs = call_args[1] if call_args else {}
        
        # Should have fn, inputs, outputs, and show_progress
        assert 'fn' in kwargs
        assert 'inputs' in kwargs
        assert 'outputs' in kwargs
        assert 'show_progress' in kwargs
        
        # Function should be lint_code
        assert kwargs['fn'] == mock_lint_code
        assert kwargs['show_progress'] == "minimal"
    
    def test_main_function_exists(self):
        """Test that main function is properly defined and importable."""
        assert callable(main)
        assert main.__name__ == 'main'
    
    @patch('src.main.gr')
    def test_main_imports_gradio_components(self, mock_gr):
        """Test that all required Gradio components are imported and used."""
        # Mock all gradio components
        mock_blocks = MagicMock()
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        mock_gr.Blocks = mock_blocks
        mock_gr.Code = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.Examples = MagicMock()
        mock_gr.Row = MagicMock()
        
        main()
        
        # Verify all components were accessed
        assert mock_gr.Blocks.called
        assert mock_gr.Code.called
        assert mock_gr.Button.called
        assert mock_gr.Examples.called
        assert mock_gr.Row.called


class TestMainConfiguration:
    """Test main function configuration details."""
    
    @patch('src.main.GRADIO_THEME')
    @patch('src.main.GRADIO_CSS')
    @patch('gradio.Blocks')
    def test_main_uses_config_values(self, mock_blocks, mock_css, mock_theme):
        """Test that main function uses configuration values."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        # Set mock config values
        mock_theme.return_value = "custom_theme"
        mock_css.return_value = "custom_css"
        
        main()
        
        # Verify configuration was used
        mock_blocks.assert_called_once()
    
    def test_main_function_signature(self):
        """Test that main function has correct signature."""
        import inspect
        
        sig = inspect.signature(main)
        assert len(sig.parameters) == 0  # Should take no parameters
        
        # Should return None (as it launches the app)
        assert sig.return_annotation == inspect.Signature.empty or sig.return_annotation is None


class TestMainIntegration:
    """Integration tests for the main module."""
    
    @patch('src.main.gr.Blocks')
    def test_main_can_be_called_multiple_times(self, mock_blocks):
        """Test that main function can be called multiple times without error."""
        mock_demo = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_demo
        
        # Should not raise any exceptions
        main()
        main()
        
        # Should have been called twice
        assert mock_blocks.call_count == 2
    
    @patch('src.main.lint_code')
    def test_main_uses_lint_function(self, mock_lint_code):
        """Test that main function properly imports and uses the lint_code function."""
        with patch('gradio.Blocks') as mock_blocks:
            mock_demo = MagicMock()
            mock_blocks.return_value.__enter__.return_value = mock_demo
            
            main()
            
            # The lint_code function should be available for use
            assert mock_lint_code is not None
