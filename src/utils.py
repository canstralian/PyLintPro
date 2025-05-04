# src/utils.py

import subprocess
import tempfile
import logging
from pathlib import Path
import yaml
from typing import List, Dict, Any, Tuple, Optional

def safe_run(
    cmd: List[str],
    cwd: Optional[Path] = None,
    timeout: int = 30
) -> Tuple[int, str, str]:
    """
    Execute an external command securely without a shell.
    Returns a tuple of (returncode, stdout, stderr).
    """
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,      # Prevent shell injection risks
        timeout=timeout
    )
    return result.returncode, result.stdout, result.stderr

def parse_flake8_output(output: str) -> List[Dict[str, Any]]:
    """
    Parse Flake8 stdout into structured records.
    Each record contains: file, line, column, code, message.
    """
    issues = []
    for line in output.splitlines():
        # Expected format: path:line:col: CODE message
        parts = line.split(":", 3)
        if len(parts) == 4:
            file_path, line_no, col_no, rest = parts
            code, message = rest.strip().split(" ", 1)
            issues.append({
                "file": file_path,
                "line": int(line_no),
                "column": int(col_no),
                "code": code,
                "message": message
            })
    return issues

def format_issues_for_display(issues: List[Dict[str, Any]]) -> str:
    """
    Convert structured Flake8 issues into a human-readable string.
    """
    if not issues:
        return "No linting issues found."
    lines = []
    for issue in issues:
        lines.append(
            f"{issue['file']}:{issue['line']}:{issue['column']} "
            f"[{issue['code']}] {issue['message']}"
        )
    return "\n".join(lines)

def load_examples(examples_dir: Path) -> List[str]:
    """
    Read all `.py` files in a directory and return their contents as examples.
    """
    snippets = []
    if examples_dir.is_dir():
        for py_file in sorted(examples_dir.glob("*.py")):
            snippets.append(py_file.read_text())
    return snippets

def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file into a Python dictionary.
    """
    with config_path.open("r") as f:
        return yaml.safe_load(f)

def setup_logging(
    name: str = __name__,
    level: str = "INFO",
    fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> None:
    """
    Configure the root logger with a consistent format and level.
    """
    logging.basicConfig(level=level, format=fmt)
    logging.getLogger(name).debug("Logging configured for %s at %s level", name, level)
