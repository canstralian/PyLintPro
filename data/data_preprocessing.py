#!/usr/bin/env python3
# data/data_preprocessing.py

"""
Data Preprocessing for PyLintPro

Uses sklearn's ColumnTransformer to handle missing values and encode categorical
features, with a CLI interface via Click.
"""

import logging
from pathlib import Path
from typing import Optional, Union, List

import click
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load dataset from a CSV file."""
    file_path = Path(file_path)
    logger.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path)
    logger.info("Data shape: %s", df.shape)
    return df


def build_preprocessing_pipeline(
    df: pd.DataFrame,
    numerical_strategy: str = "median",
    categorical_strategy: str = "most_frequent",
    encoding: str = "onehot",
    handle_unknown: str = "ignore"
) -> ColumnTransformer:
    """
    Create a ColumnTransformer that:
      - Imputes numeric columns with median/mean/constant
      - Imputes categorical columns with most_frequent/constant
      - Encodes categoricals via OneHot or Ordinal

    Args:
        df: Input DataFrame to determine column types
        numerical_strategy: Strategy for numeric imputation
        categorical_strategy: Strategy for categorical imputation
        encoding: Encoding method ('onehot' or 'ordinal')
        handle_unknown: How to handle unknown categories
    """
    # Pre-compute column lists once instead of using lambdas
    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()
    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # Numeric imputer
    num_imputer = SimpleImputer(strategy=numerical_strategy)

    # Categorical pipeline
    if encoding == "onehot":
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy=categorical_strategy)),
            ("encoder", OneHotEncoder(
                handle_unknown=handle_unknown, sparse=False))
        ])
    else:
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy=categorical_strategy)),
            ("encoder", OrdinalEncoder())
        ])

    # Build ColumnTransformer with pre-computed column lists
    preprocessing = ColumnTransformer(
        transformers=[
            ("num", num_imputer, numeric_cols),
            ("cat", cat_pipeline, categorical_cols)
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )

    logger.info(
        "Preprocessing pipeline constructed with %d numeric and "
        "%d categorical columns",
        len(numeric_cols), len(categorical_cols))
    return preprocessing


def preprocess_data(
    df: pd.DataFrame,
    pipeline: ColumnTransformer
) -> pd.DataFrame:
    """
    Fit the pipeline on df and return a transformed DataFrame
    with automatically generated feature names.

    Args:
        df: Input DataFrame
        pipeline: ColumnTransformer pipeline
    """
    # Determine feature names after transform
    pipeline.fit(df)
    feature_names = pipeline.get_feature_names_out()
    data = pipeline.transform(df)
    processed_df = pd.DataFrame(data, columns=feature_names, index=df.index)
    logger.info("Processed data with shape %s", processed_df.shape)
    return processed_df


@click.command()
@click.option("--input-file", "-i", type=click.Path(exists=True),
              required=True, help="Path to input CSV file")
@click.option("--output-file", "-o", type=click.Path(),
              required=True, help="Path for output CSV file")
@click.option("--num-strat", default="median",
              help="Imputation strategy for numeric columns")
@click.option("--cat-strat", default="most_frequent",
              help="Imputation strategy for categorical")
@click.option("--encoding", type=click.Choice(["onehot", "ordinal"]),
              default="onehot", help="Encoding method for categorical features")
def main(input_file: str, output_file: str, num_strat: str,
         cat_strat: str, encoding: str):
    """CLI entry point for data preprocessing."""
    df = load_data(input_file)
    pipeline = build_preprocessing_pipeline(
        df,
        numerical_strategy=num_strat,
        categorical_strategy=cat_strat,
        encoding=encoding
    )
    processed_df = preprocess_data(df, pipeline)
    processed_df.to_csv(output_file, index=False)
    logger.info("Saved processed data to %s", output_file)


if __name__ == "__main__":
    main()
