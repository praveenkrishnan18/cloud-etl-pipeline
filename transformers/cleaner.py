"""
transformers/cleaner.py — Cleans and reshapes raw API records
Keeps only needed fields, normalises text, drops nulls.
"""

from utils.logger import get_logger

logger = get_logger(__name__)


def clean_and_transform(raw_records: list[dict]) -> list[dict]:
    """
    Input  : raw list of dicts straight from the API
    Output : cleaned list of dicts ready for storage

    Rules applied here (customise for your API):
      - Keep only: id, userId, title, body
      - Strip leading/trailing whitespace from text fields
      - Drop any record that is missing 'id' or 'title'
      - Add a derived field: title_word_count
    """
    cleaned = []

    for record in raw_records:
        # --- Guard: skip malformed records ---
        if not record.get("id") or not record.get("title"):
            logger.warning(f"Skipping record missing id/title: {record}")
            continue

        cleaned.append({
            "id":               record["id"],
            "user_id":          record.get("userId"),
            "title":            record["title"].strip(),
            "body":             record.get("body", "").strip(),
            "title_word_count": len(record["title"].split()),   # derived field
        })

    dropped = len(raw_records) - len(cleaned)
    if dropped:
        logger.warning(f"Dropped {dropped} invalid records during transformation.")

    return cleaned
