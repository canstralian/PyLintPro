# src/lint.py

import tempfile
import os
import logging
from typing import Tuple
from .utils import safe_run, parse_flake8_output, format_issues_for_display

logger = logging.getLogger(__name__)

# Try to import autopep8, fall back to simple formatting if not available
try:
    import autopep8
    AUTOPEP8_AVAILABLE = True
except ImportError:
    AUTOPEP8_AVAILABLE = False
    logger.warning("autopep8 not available, using simple formatting")


def simple_format_code(code: str) -> str:
    """
    Simple code formatting as fallback when autopep8 is not available.
    """
    if not code.strip():
        return code
    
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Keep empty lines as is
        if not line.strip():
            formatted_lines.append('')
            continue
            
        # Get the original indentation
        indent = len(line) - len(line.lstrip())
        content = line.strip()
        
        # Fix spacing issues in function calls like print( 'hello' )
        # Remove extra spaces after opening parentheses and before closing ones
        content = content.replace('( ', '(').replace(' )', ')')
        content = content.replace('[ ', '[').replace(' ]', ']')
        content = content.replace('{ ', '{').replace(' }', '}')
        
        # Basic spacing fixes (be more careful)
        # Fix spacing around = but not in ==, !=, <=, >=
        if ' = ' not in content and '==' not in content and '!=' not in content and '<=' not in content and '>=' not in content:
            content = content.replace('=', ' = ')
        
        # Fix spacing around commas  
        content = content.replace(',', ', ')
        
        # Clean up double spaces
        while '  ' in content:
            content = content.replace('  ', ' ')
        
        # Preserve the original indentation and append formatted content
        formatted_lines.append(' ' * indent + content)
    
    return '\n'.join(formatted_lines)


def lint_code(code: str) -> str:
    """
    Formats code with autopep8 and runs flake8 to collect linting issues.
    Returns the formatted code plus any flake8 warnings.
    
    Args:
        code: The Python code to format and lint
        
    Returns:
        A string containing the formatted code and any flake8 issues
    """
    logger.info("Starting code linting process")
    
    try:
        # Format with autopep8 or simple formatting
        logger.debug("Formatting code")
        if AUTOPEP8_AVAILABLE:
            try:
                formatted_code = autopep8.fix_code(code, options={"aggressive": 1})
            except Exception as e:
                logger.warning(f"autopep8 failed: {e}, falling back to simple formatting")
                formatted_code = simple_format_code(code)
        else:
            formatted_code = simple_format_code(code)
        
        # Write to temp file for flake8
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
            tmp.write(formatted_code)
            tmp_path = tmp.name
        
        logger.debug(f"Created temporary file: {tmp_path}")
        
        # Run flake8 using safe_run utility
        returncode, stdout, stderr = safe_run(["flake8", tmp_path])
        
        # Clean up temp file
        os.unlink(tmp_path)
        logger.debug(f"Cleaned up temporary file: {tmp_path}")
        
        if returncode == 0:
            issues_message = "No linting issues found."
            logger.info("Code linting completed successfully with no issues")
        else:
            # Parse flake8 output for better formatting
            parsed_issues = parse_flake8_output(stdout)
            issues_message = format_issues_for_display(parsed_issues)
            logger.info(f"Code linting completed with {len(parsed_issues)} issues found")
        
        result = f"{formatted_code}\n\n# Flake8 issues:\n{issues_message}"
        
        if stderr:
            logger.warning(f"Flake8 stderr: {stderr}")
            result += f"\n\n# Warnings:\n{stderr}"
            
        return result
        
    except Exception as e:
        logger.error(f"Error during code linting: {str(e)}")
        return f"Error processing code: {str(e)}"


def format_code_only(code: str) -> str:
    """
    Format code with autopep8 or simple formatting without running flake8.
    
    Args:
        code: The Python code to format
        
    Returns:
        The formatted code
    """
    logger.info("Formatting code only (no linting)")
    
    try:
        if AUTOPEP8_AVAILABLE:
            try:
                formatted_code = autopep8.fix_code(code, options={"aggressive": 1})
            except Exception as e:
                logger.warning(f"autopep8 failed: {e}, falling back to simple formatting")
                formatted_code = simple_format_code(code)
        else:
            formatted_code = simple_format_code(code)
            
        logger.info("Code formatting completed successfully")
        return formatted_code
    except Exception as e:
        logger.error(f"Error during code formatting: {str(e)}")
        return f"Error formatting code: {str(e)}"


def check_code_only(code: str) -> Tuple[bool, str]:
    """
    Check code with flake8 without formatting.
    
    Args:
        code: The Python code to check
        
    Returns:
        A tuple of (is_clean, issues_report)
    """
    logger.info("Checking code for linting issues only")
    
    try:
        # Write to temp file for flake8
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        
        logger.debug(f"Created temporary file: {tmp_path}")
        
        # Run flake8 using safe_run utility
        returncode, stdout, stderr = safe_run(["flake8", tmp_path])
        
        # Clean up temp file
        os.unlink(tmp_path)
        logger.debug(f"Cleaned up temporary file: {tmp_path}")
        
        if returncode == 0:
            logger.info("Code check completed successfully with no issues")
            return True, "No linting issues found."
        else:
            # Parse flake8 output for better formatting
            parsed_issues = parse_flake8_output(stdout)
            issues_message = format_issues_for_display(parsed_issues)
            logger.info(f"Code check completed with {len(parsed_issues)} issues found")
            return False, issues_message
            
    except Exception as e:
        logger.error(f"Error during code checking: {str(e)}")
        return False, f"Error checking code: {str(e)}"