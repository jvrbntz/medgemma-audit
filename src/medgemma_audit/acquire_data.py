"""
Acquire the MTSamples dataset via kagglehub and save it into data/.

"""

import argparse
import logging
import shutil
from pathlib import Path

import kagglehub

DATASET_HANDLE = "tboyle10/medicaltranscriptions"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
EXPECTED_FILENAME = "mtsamples.csv"

logger = logging.getLogger(__name__)


def acquire(force: bool = False) -> Path:
    """Download the MTSamples dataset via kagglehub and copy it into data/.

    Idempotent by default: skips the download if the file is already
    present locally. Returns the path to the saved CSV.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target_path = DATA_DIR / EXPECTED_FILENAME

    if target_path.exists() and not force:
        logger.info(
            "Dataset already present at %s, skipping download (use --force to re-download).",
            target_path,
        )
        return target_path

    logger.info("Downloading dataset '%s' via kagglehub...", DATASET_HANDLE)
    try:
        cache_path = Path(kagglehub.dataset_download(DATASET_HANDLE))
    except Exception as exc:
        raise RuntimeError(
            f"Failed to download dataset '{DATASET_HANDLE}' via kagglehub. "
            "Check that Kaggle credentials are configured "
            "(~/.kaggle/kaggle.json or KAGGLE_USERNAME/KAGGLE_KEY env vars)."
        ) from exc

    source_file = cache_path / EXPECTED_FILENAME
    if not source_file.exists():
        csv_files = list(cache_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(
                f"No CSV file found in downloaded dataset at {cache_path}"
            )
        source_file = csv_files[0]
        logger.warning(
            "Expected filename '%s' not found; using '%s' instead.",
            EXPECTED_FILENAME,
            source_file.name,
        )

    if source_file.stat().st_size == 0:
        raise ValueError(f"Downloaded file {source_file} is empty.")

    shutil.copy2(source_file, target_path)
    logger.info(
        "Saved dataset to %s (%d bytes).", target_path, target_path.stat().st_size
    )
    return target_path


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if the file already exists.",
    )
    args = parser.parse_args()
    acquire(force=args.force)


if __name__ == "__main__":
    main()
