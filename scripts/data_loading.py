# data_loading.py
from datasets import load_dataset

def load_datasets():
    """Load and return the datasets."""
    ds_edge_case = load_dataset("cchoi1/pylint_edge_case_dedup_cleaned_1")
    ds_logic_multifile = load_dataset("cchoi1/pylint_logic_multifile_codebase_100")
    ds_logic_multifile_dedup = load_dataset("cchoi1/pylint_logic_multifile_codebase_dedup_99")
    return ds_edge_case, ds_logic_multifile, ds_logic_multifile_dedup
