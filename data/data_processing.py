"""
Data Processing for PyLintPro

Scales numeric features and generates polynomial interaction terms via
a unified sklearn Pipeline, with a CLI interface via Click.
"""

import logging
from pathlib import Path
from typing import List, Union

import click
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Read CSV into DataFrame."""
    file_path = Path(file_path)
    logger.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path)
    logger.info("Data shape: %s", df.shape)
    return df


@click.command()
@click.option("--input-file", "-i", type=click.Path(exists=True),
              required=True, help="Path to input CSV file")
@click.option("--output-file", "-o", type=click.Path(),
              required=True, help="Path for output CSV file")
@click.option("--degree", "-d", default=2, show_default=True,
              help="Degree of polynomial features to generate")
@click.option("--columns", "-c", multiple=True,
              help="Explicit list of columns; defaults to all numeric")
def main(input_file: str, output_file: str, degree: int, columns: List[str]):
    """CLI entry point for data processing."""
    df = load_data(input_file)

    # Optimize column selection - only compute once
    if columns:
        numeric_cols = list(columns)
    else:
        numeric_cols = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

    logger.info("Preparing pipeline for %d columns", len(numeric_cols))

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("poly", PolynomialFeatures(
            degree=degree, include_bias=False
        ))
    ])

    # Fit-transform only the selected columns
    arr = pipeline.fit_transform(df[numeric_cols])
    feature_names = pipeline.named_steps["poly"].get_feature_names_out(
        numeric_cols)

    df_poly = pd.DataFrame(arr, columns=feature_names, index=df.index)
    result_df = df.join(df_poly)
    result_df.to_csv(output_file, index=False)
    logger.info("Saved processed data with polynomial features to %s",
                output_file)


if __name__ == "__main__":
    main()
