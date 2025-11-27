#!/usr/bin/env python3
# data/utils.py

"""
Centralized data utilities for PyLintPro

Common functions for data loading and processing operations.
"""

import logging
from pathlib import Path
from typing import Union

import pandas as pd

logger = logging.getLogger(__name__)


def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load dataset from a CSV file.

    Args:
        file_path: Path to the CSV file to load

    Returns:
        DataFrame containing the loaded data
    """
    file_path = Path(file_path)
    logger.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path)
    logger.info("Data shape: %s", df.shape)
    return df
