# src/data_loading.py

import os
import logging
from pathlib import Path
from typing import List, Union, Dict, Optional
from datasets import load_dataset, DatasetDict, IterableDataset
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure module-level logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

def buffered_stream(
    iterable: IterableDataset,
    prefetch: int = 2,
    max_workers: int = 4
) -> IterableDataset:
    """
    Wrap an IterableDataset to prefetch batches using ThreadPoolExecutor.
    """
    def generator():
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            iterator = iter(iterable)
            # Prefill buffer
            for _ in range(prefetch):
                try:
                    futures.append(executor.submit(next, iterator))
                except StopIteration:
                    break
            while futures:
                # Yield the first completed batch
                done, futures[:] = [f for f in futures if f.done()], [f for f in futures if not f.done()]
                for future in done:
                    yield future.result()
                    # Submit next
                    try:
                        futures.append(executor.submit(next, iterator))
                    except StopIteration:
                        continue
    return IterableDataset.from_generator(generator)

def load_datasets(
    dataset_names: Union[str, List[str]],
    *,
    streaming: bool = False,
    cache_dir: Optional[Union[str, Path]] = None,
    use_auth_token: bool = False,
    download_mode: str = "reuse_cache_if_exists",
    split: Optional[str] = None,
    enable_progress: bool = True,
    prefetch_buffer: int = 2,
    max_workers: int = 4
) -> Dict[str, Union[DatasetDict, IterableDataset]]:
    """
    Load one or more Hugging Face datasets with flexible options.

    Args:
        dataset_names: Single or list of dataset identifiers on HF Hub.
        streaming: If True, returns IterableDataset streams; else DatasetDict.
        cache_dir: Directory for caching; overrides HF_DATASETS_CACHE.
        use_auth_token: Pass HF token for private datasets.
        download_mode: 'reuse_cache_if_exists' or 'force_redownload'.
        split: Optional split spec (e.g., 'train[:10%]').
        enable_progress: Toggle tqdm progress bars.
        prefetch_buffer: Number of batches to prefetch for IterableDataset.
        max_workers: Threads for prefetching.

    Returns:
        Mapping from dataset name to loaded DatasetDict or IterableDataset.
    """
    if isinstance(dataset_names, str):
        dataset_names = [dataset_names]

    if cache_dir:
        os.environ["HF_DATASETS_CACHE"] = str(cache_dir)

    from datasets import set_progress_bar_enabled
    set_progress_bar_enabled(enable_progress)

    loaded: Dict[str, Union[DatasetDict, IterableDataset]] = {}
    for name in dataset_names:
        try:
            logger.info("Loading '%s' (streaming=%s, split=%s)", name, streaming, split)
            ds = load_dataset(
                path=name,
                split=split,
                streaming=streaming,
                cache_dir=str(cache_dir) if cache_dir else None,
                use_auth_token=use_auth_token,
                download_mode=download_mode
            )
            if streaming and prefetch_buffer > 0:
                ds = buffered_stream(ds, prefetch=prefetch_buffer, max_workers=max_workers)
                logger.info("Applied prefetch buffer=%d, workers=%d", prefetch_buffer, max_workers)
            loaded[name] = ds
            logger.info("Successfully loaded '%s'", name)
        except Exception as e:
            logger.error("Failed to load '%s': %s", name, e)
            raise
    return loaded

# Example usage
if __name__ == "__main__":
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
        split="train[:10%]",
        enable_progress=True,
        prefetch_buffer=3,
        max_workers=2
    )
    for key, ds in datasets.items():
        # DatasetDict prints split names; IterableDataset prints class info
        print(f"{key}: {ds}")
