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
    df = pd.read_csv(file_path)  # pandas.read_csv 
    logger.info("Data shape: %s", df.shape)
    return df

def build_preprocessing_pipeline(
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
    """
    # Numeric imputer
    num_imputer = SimpleImputer(strategy=numerical_strategy)  # sklearn.impute.SimpleImputer  [oai_citation_attribution:0‡Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html?utm_source=chatgpt.com)

    # Categorical pipeline
    if encoding == "onehot":
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy=categorical_strategy)),
            ("encoder", OneHotEncoder(handle_unknown=handle_unknown, sparse=False))
        ])  # sklearn.preprocessing.OneHotEncoder  [oai_citation_attribution:1‡Scikit-learn](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html?utm_source=chatgpt.com)
    else:
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy=categorical_strategy)),
            ("encoder", OrdinalEncoder())
        ])  # sklearn.preprocessing.OrdinalEncoder  [oai_citation_attribution:2‡MachineLearningMastery.com](https://machinelearningmastery.com/columntransformer-for-numerical-and-categorical-data/?utm_source=chatgpt.com)

    # Build ColumnTransformer
    preprocessing = ColumnTransformer(
        transformers=[
            ("num", num_imputer, 
             lambda df: df.select_dtypes(include=["int64", "float64"]).columns.tolist()),
            ("cat", cat_pipeline, 
             lambda df: df.select_dtypes(include=["object", "category"]).columns.tolist())
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )  # sklearn.compose.ColumnTransformer  [oai_citation_attribution:3‡Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html?utm_source=chatgpt.com)

    logger.info("Preprocessing pipeline constructed")
    return preprocessing

def preprocess_data(
    df: pd.DataFrame,
    pipeline: ColumnTransformer
) -> pd.DataFrame:
    """
    Fit the pipeline on df and return a transformed DataFrame
    with automatically generated feature names.
    """
    # Determine feature names after transform
    pipeline.fit(df)
    feature_names = pipeline.get_feature_names_out()  # Requires sklearn ≥1.2  [oai_citation_attribution:4‡Stack Overflow](https://stackoverflow.com/questions/70933014/how-to-use-columntransformer-to-return-a-dataframe?utm_source=chatgpt.com)
    data = pipeline.transform(df)
    processed_df = pd.DataFrame(data, columns=feature_names, index=df.index)
    logger.info("Processed data with shape %s", processed_df.shape)
    return processed_df

@click.command()
@click.option("--input-file", "-i", type=click.Path(exists=True), required=True,
              help="Path to input CSV file")  # click CLI  [oai_citation_attribution:5‡Click Documentation](https://click.palletsprojects.com/en/stable/?utm_source=chatgpt.com)
@click.option("--output-file", "-o", type=click.Path(), required=True,
              help="Path for output CSV file")
@click.option("--num-strat", default="median",
              help="Imputation strategy for numeric columns (mean|median|constant)")
@click.option("--cat-strat", default="most_frequent",
              help="Imputation strategy for categorical (most_frequent|constant)")
@click.option("--encoding", type=click.Choice(["onehot", "ordinal"]), default="onehot",
              help="Encoding method for categorical features")
def main(input_file: str, output_file: str, num_strat: str, cat_strat: str, encoding: str):
    """CLI entry point for data preprocessing."""
    df = load_data(input_file)
    pipeline = build_preprocessing_pipeline(
        numerical_strategy=num_strat,
        categorical_strategy=cat_strat,
        encoding=encoding
    )
    processed_df = preprocess_data(df, pipeline)
    processed_df.to_csv(output_file, index=False)
    logger.info("Saved processed data to %s", output_file)

if __name__ == "__main__":
    main()