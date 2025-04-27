# scripts/preprocess.py

import argparse
import logging
import json
from pathlib import Path

from datasets import load_dataset, set_progress_bar_enabled
from src.lint import lint_code
from src.utils import parse_flake8_output

def preprocess_example(example: dict) -> dict:
    """
    Apply lint_code to a single example, splitting out formatted code and issues.
    """
    # Extract code field (adjust key if your dataset uses a different field name)
    code = example.get("code") or example.get("text") or ""
    # lint_code returns formatted code plus a Flake8 issues section
    result = lint_code(code)
    if "# Flake8 issues:\n" in result:
        formatted, issues_str = result.split("# Flake8 issues:\n", 1)
    else:
        formatted, issues_str = result, ""
    # Parse the Flake8 output into structured data
    issues = parse_flake8_output(issues_str)
    return {
        "original_code": code,
        "formatted_code": formatted,
        "issues": issues
    }

def main():
    parser = argparse.ArgumentParser(
        description="Preprocess a Hugging Face dataset with PyLintPro linting."
    )
    parser.add_argument(
        "--dataset", type=str, required=True,
        help="Hugging Face dataset identifier (e.g., 'cchoi1/pylint_edge_case_dedup_cleaned_1')"
    )
    parser.add_argument(
        "--split", type=str, default="train",
        help="Dataset split to preprocess (default: 'train')"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("preprocessed.jsonl"),
        help="Path to output JSONL file (default: preprocessed.jsonl)"
    )
    parser.add_argument(
        "--batch_size", type=int, default=1000,
        help="Batch size for map() (default: 1000)"
    )
    parser.add_argument(
        "--num_proc", type=int, default=1,
        help="Number of parallel processes for map() (default: 1)"
    )
    parser.add_argument(
        "--disable_progress", action="store_true",
        help="Disable the progress bar (useful for CI or non-interactive runs)"
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    set_progress_bar_enabled(not args.disable_progress)

    logging.info("Loading dataset %s (split=%s)", args.dataset, args.split)
    ds = load_dataset(args.dataset, split=args.split)

    logging.info(
        "Starting preprocessing: batch_size=%d, num_proc=%d",
        args.batch_size, args.num_proc
    )
    processed = ds.map(
        preprocess_example,
        batched=False,
        batch_size=args.batch_size,
        num_proc=args.num_proc,
        remove_columns=ds.column_names,
        desc="Preprocessing examples"
    )

    logging.info("Writing preprocessed data to %s", args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        for record in processed:
            f.write(json.dumps(record) + "\n")

    logging.info("Preprocessing complete. %d records written.", len(processed))

if __name__ == "__main__":
    main()