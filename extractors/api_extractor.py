"""
extractors/api_extractor.py — Pulls raw data from a public REST API
Example uses: https://jsonplaceholder.typicode.com/posts  (free, no auth needed)
Swap the URL for any real open API (weather, crypto, etc.)
"""

import requests
from utils.logger import get_logger

logger = get_logger(__name__)

API_URL = "https://jsonplaceholder.typicode.com/posts"   # ← swap your API here
TIMEOUT_SECONDS = 10


def fetch_data() -> list[dict]:
    """
    Fetch JSON records from the configured API.
    Returns a list of dicts.
    Raises requests.HTTPError on non-2xx status codes.
    """
    logger.info(f"GET {API_URL}")
    response = requests.get(API_URL, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()          # throws HTTPError if status >= 400

    data = response.json()
    logger.info(f"API returned {len(data)} raw records.")
    return data
