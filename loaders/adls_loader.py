"""
loaders/adls_loader.py — Uploads transformed data to Azure ADLS Gen2 as CSV

CHANGES FROM v1:
  1. Output format  : JSON → CSV (proper tabular format, readable in Excel/Synapse)
  2. Folder layout  : was creating nested sub-folders (pipeline/output/...)
                      now writes directly into one flat output folder.
                      Set ADLS_OUTPUT_FOLDER in your .env / GitHub Secrets.

CREDENTIALS STRATEGY (zero secrets in code):
  Local dev       → .env file (never commit it — it's in .gitignore)
  GitHub Actions  → Repository Secrets, injected as env vars at runtime
"""

from dotenv import load_dotenv
load_dotenv()

import csv
import io
import os
from datetime import datetime, timezone

from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import AzureError

from utils.logger import get_logger

logger = get_logger(__name__)

# ── Config — all values come from environment, never hard-coded ──────────────
ACCOUNT_NAME   = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
ACCOUNT_KEY    = os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
FILESYSTEM     = os.environ.get("ADLS_FILESYSTEM_NAME", "raw")
OUTPUT_FOLDER  = os.environ.get("ADLS_OUTPUT_FOLDER", "output")   # single flat folder
# ─────────────────────────────────────────────────────────────────────────────

# Columns written to CSV — must match keys produced by cleaner.py
CSV_COLUMNS = ["id", "user_id", "title", "body", "title_word_count"]


def _build_file_name() -> str:
    """Timestamped filename so each run produces a new file, never overwrites."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"data_{ts}.csv"


def _records_to_csv(records: list[dict]) -> bytes:
    """
    Convert a list of cleaned dicts → UTF-8 CSV bytes.
    Uses the fixed column order in CSV_COLUMNS so the header is always stable.
    """
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=CSV_COLUMNS,
        extrasaction="ignore",   # silently drop any unexpected keys
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue().encode("utf-8")


def upload_to_adls(records: list[dict]) -> None:
    """
    Upload `records` as a CSV file into a single flat folder on ADLS Gen2.

    Path written:
        {FILESYSTEM}/{OUTPUT_FOLDER}/data_{timestamp}.csv

    No sub-folders are created — only one directory level under the container.
    """
    try:
        # 1. Connect
        service_client = DataLakeServiceClient(
            account_url=f"https://{ACCOUNT_NAME}.dfs.core.windows.net",
            credential=ACCOUNT_KEY,
        )

        # 2. Get the filesystem (container)
        fs_client = service_client.get_file_system_client(FILESYSTEM)

        # 3. Ensure the single output folder exists (no-op if already there)
        dir_client = fs_client.get_directory_client(OUTPUT_FOLDER)
        dir_client.create_directory()

        # 4. Build the CSV payload
        payload   = _records_to_csv(records)
        file_name = _build_file_name()

        # 5. Upload directly into that one folder — no nested paths
        file_client = dir_client.create_file(file_name)
        file_client.upload_data(payload, overwrite=True)

        full_path = f"{FILESYSTEM}/{OUTPUT_FOLDER}/{file_name}"
        logger.info(f"Uploaded {len(records)} rows as CSV → adls://{full_path}")

    except KeyError as e:
        raise EnvironmentError(
            f"Missing required environment variable: {e}. "
            "Add it to your .env (local) or GitHub Secrets (CI)."
        ) from e

    except AzureError as e:
        raise RuntimeError(f"Azure upload failed: {e}") from e