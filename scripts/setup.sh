#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# PyLintPro Environment Setup Script
# ------------------------------------------------------------------------------

# Exit immediately on errors, undefined vars, or failed pipes (Unofficial Bash Strict Mode)
set -euo pipefail   #  [oai_citation_attribution:0‡redsymbol.net](https://redsymbol.net/articles/unofficial-bash-strict-mode/?utm_source=chatgpt.com)
IFS=$'\n\t'

# Determine project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 1. Create & activate Python virtual environment
VENV_DIR="$PROJECT_ROOT/.venv"
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating virtual environment in $VENV_DIR..."
  python3 -m venv "$VENV_DIR"    #  [oai_citation_attribution:1‡packaging.python.org](https://packaging.python.org/en/latest/specifications/virtual-environments/?utm_source=chatgpt.com)
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# 2. Upgrade pip and install Python dependencies
echo "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip   #  [oai_citation_attribution:2‡pip.pypa.io](https://pip.pypa.io/en/stable/installation/?utm_source=chatgpt.com)
pip install -r "$PROJECT_ROOT/requirements.txt"

# 3. Make utility scripts executable
echo "Making backend scripts executable..."
chmod +x "$PROJECT_ROOT/scripts/"*.py

# 4. (Optional) Install pre-commit hooks if available
if command -v pre-commit &> /dev/null; then
  echo "Installing pre-commit hooks..."
  pre-commit install
fi

echo
echo "Setup complete!"
echo "  • Activate your environment with:  source $VENV_DIR/bin/activate"
echo "  • To run the backend API:           ./scripts/run_backend.py"
echo "  • To run preprocessing:             ./scripts/preprocess.py"
echo "  • To generate GitHub summary:       ./scripts/github_summary.py"