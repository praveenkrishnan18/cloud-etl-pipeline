"""
tests/test_cleaner.py — Unit tests for the transformer layer
Run locally:  pytest tests/
"""

import pytest
from transformers.cleaner import clean_and_transform


# ── Fixtures ──────────────────────────────────────────────────────────────────

VALID_RECORDS = [
    {"id": 1, "userId": 10, "title": "  Hello World  ", "body": "some text"},
    {"id": 2, "userId": 11, "title": "Data Engineering", "body": ""},
]

MIXED_RECORDS = [
    {"id": 3, "userId": 12, "title": "Good Record", "body": "ok"},
    {"id": None, "userId": 13, "title": "Missing ID"},          # ← should be dropped
    {"id": 4, "userId": 14, "title": "", "body": "no title"},   # ← should be dropped
]


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_returns_list():
    result = clean_and_transform(VALID_RECORDS)
    assert isinstance(result, list)


def test_whitespace_stripped():
    result = clean_and_transform(VALID_RECORDS)
    assert result[0]["title"] == "Hello World"          # stripped


def test_word_count_computed():
    result = clean_and_transform(VALID_RECORDS)
    assert result[0]["title_word_count"] == 2           # "Hello World"
    assert result[1]["title_word_count"] == 2           # "Data Engineering"


def test_invalid_records_dropped():
    result = clean_and_transform(MIXED_RECORDS)
    assert len(result) == 1                             # only "Good Record" survives
    assert result[0]["id"] == 3


def test_empty_input():
    assert clean_and_transform([]) == []


def test_field_mapping():
    result = clean_and_transform(VALID_RECORDS)
    record = result[0]
    assert "user_id" in record                          # userId → user_id
    assert "userId" not in record                       # original key removed
