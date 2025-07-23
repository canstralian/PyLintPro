#!/usr/bin/env python3
"""
PyLintPro CLI - Command line interface for Python code linting and formatting.
"""

import argparse
import autopep8
import subprocess
import sys
import os
from pathlib import Path


def lint_file(file_path, ignore_rules=None, output_path=None):
    """
    Lint and format a Python file using autopep8 and flake8.

    Args:
        file_path (str): Path to the Python file to lint
        ignore_rules (str): Comma-separated list of flake8 rules to ignore
        output_path (str): Path to save the corrected output

    Returns:
        tuple: (formatted_code, flake8_issues)
    """
    try:
        # Read the input file
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Try to format with autopep8, fall back to original code if it fails
        try:
            formatted_code = autopep8.fix_code(code, options={"aggressive": 1})
        except Exception as e:
            print(f"Warning: autopep8 formatting failed ({e}), "
                  "using original code")
            formatted_code = code

        # Prepare flake8 command
        flake8_cmd = ["flake8", file_path]
        if ignore_rules:
            flake8_cmd.extend(["--ignore", ignore_rules])

        # Run flake8
        result = subprocess.run(
            flake8_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        flake8_issues = result.stdout.strip() or "No issues found."

        # Save corrected output
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_code)
            print(f"Corrected code saved to: {output_path}")
        else:
            # Default output path
            file_stem = Path(file_path).stem
            file_dir = Path(file_path).parent
            default_output = file_dir / f"{file_stem}_fixed.py"
            with open(default_output, 'w', encoding='utf-8') as f:
                f.write(formatted_code)
            print(f"Corrected code saved to: {default_output}")

        return formatted_code, flake8_issues

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PyLintPro CLI - Lint and format Python code"
    )
    parser.add_argument(
        "file",
        help="Python file to lint and format"
    )
    parser.add_argument(
        "--ignore",
        help="Comma-separated list of flake8 rules to ignore (e.g., E501,W503)"
    )
    parser.add_argument(
        "--output",
        help="Custom output path for the corrected code"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Check if file exists
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        sys.exit(1)

    # Check if it's a Python file
    if not args.file.endswith('.py'):
        print("Warning: File does not have .py extension")

    print(f"Processing: {args.file}")
    if args.ignore:
        print(f"Ignoring rules: {args.ignore}")

    # Process the file
    formatted_code, flake8_issues = lint_file(
        args.file,
        ignore_rules=args.ignore,
        output_path=args.output
    )

    # Display results
    print("\n" + "="*50)
    print("LINTING RESULTS")
    print("="*50)
    print(flake8_issues)

    if args.verbose:
        print("\n" + "="*50)
        print("FORMATTED CODE PREVIEW")
        print("="*50)
        print(formatted_code[:500] + "..." if len(formatted_code) > 500
              else formatted_code)


if __name__ == "__main__":
    main()
