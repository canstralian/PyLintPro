from datasets import load_dataset, IterableDataset, DatasetDict
from pathlib import Path
import logging
import os
from typing import Dict, Union, Optional

# Configure module-level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def load_datasets(
    dataset_names: Union[str, list[str]],
    *,
    streaming: bool = False,
    cache_dir: Optional[Union[str, Path]] = None,
    use_auth_token: bool = False,
    download_mode: str = "reuse_cache_if_exists",
) -> Dict[str, Union[DatasetDict, IterableDataset]]:
    """
    Load one or more Hugging Face datasets with optional streaming, custom caching,
    and error handling. Returns a dict mapping dataset names to their loaded
    DatasetDict or IterableDataset objects.
    
    Args:
        dataset_names: A single dataset identifier or list of identifiers on the HF Hub.
        streaming: If True, returns IterableDataset streams instead of full DatasetDicts.
        cache_dir: Custom directory to cache dataset files and processing artifacts.
        use_auth_token: Whether to pass the HF token (from HUGGINGFACE_HUB_TOKEN) to private repos.
        download_mode: Mode controlling cache reuse or forced redownload.
                       Options: 'reuse_cache_if_exists', 'force_redownload'.
    
    Returns:
        A dict where keys are the dataset identifiers and values are the loaded datasets.
    """
    # Normalize to list
    if isinstance(dataset_names, str):
        dataset_names = [dataset_names]

    loaded = {}
    for name in dataset_names:
        try:
            logger.info("Loading dataset %s (streaming=%s)", name, streaming)
            ds = load_dataset(
                path=name,
                streaming=streaming,
                cache_dir=str(cache_dir) if cache_dir else None,
                use_auth_token=use_auth_token,
                download_mode=download_mode
            )
            loaded[name] = ds
            logger.info("Successfully loaded %s", name)
        except Exception as e:
            logger.error("Error loading dataset %s: %s", name, e)
            # Re‐raise or handle as needed
            raise
    return loaded


if __name__ == "__main__":
    # Example usage:
    CACHE_PATH = os.getenv("HF_DATASETS_CACHE", "./hf_cache")
    names = [
        "cchoi1/pylint_edge_case_dedup_cleaned_1",
        "cchoi1/pylint_logic_multifile_codebase_100",
        "cchoi1/pylint_logic_multifile_codebase_dedup_99"
    ]
    datasets = load_datasets(
        names,
        streaming=False,
        cache_dir=CACHE_PATH,
        use_auth_token=False,
        download_mode="reuse_cache_if_exists"
    )
    for key, ds in datasets.items():
        print(f"{key}: {ds}")