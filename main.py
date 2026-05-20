"""
main.py — Pipeline entry point
Orchestrates: Extract → Transform → Load
"""

import logging
import sys
from extractors.api_extractor import fetch_data
from transformers.cleaner import clean_and_transform
from loaders.adls_loader import upload_to_adls
from utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline():
    logger.info("======= Pipeline started =======")

    try:
        # STEP 1: Extract
        logger.info("[1/3] Extracting data from API...")
        raw_data = fetch_data()
        logger.info(f"      Extracted {len(raw_data)} records.")

        # STEP 2: Transform
        logger.info("[2/3] Cleaning and transforming data...")
        transformed_data = clean_and_transform(raw_data)
        logger.info(f"      Transformed into {len(transformed_data)} clean records.")

        # STEP 3: Load
        logger.info("[3/3] Uploading to Azure ADLS Gen2...")
        upload_to_adls(transformed_data)
        logger.info("      Upload complete.")

        logger.info("======= Pipeline finished successfully =======")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)  # Non-zero exit makes GitHub Actions mark the job as FAILED


if __name__ == "__main__":
    run_pipeline()
