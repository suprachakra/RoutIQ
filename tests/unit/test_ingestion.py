"""
Unit tests for data ingestion and cleaning modules.
Tests include:
- Verifying that null and duplicate records are removed.
- Checking proper error handling for invalid input types.
"""

import pytest
from src.services.data_ingestion.data_cleaner import clean_data

def test_clean_data_removes_null_and_duplicates():
    sample_data = [
        {"id": 1, "value": "Test"},
        None,
        {"id": 1, "value": "test"},  # Duplicate after normalization.
        {"id": 2, "value": "Example"},
        {}  # Empty record.
    ]
    cleaned = clean_data(sample_data)
    # Expect non-empty list with no None or {} records.
    assert isinstance(cleaned, list)
    for record in cleaned:
        assert record, "Record should not be empty."
    # Check that duplicate records (after normalization) are removed.
    ids = [record["id"] for record in cleaned if "id" in record]
    assert ids.count(1) == 1, "Duplicate records for id '1' should be removed."

def test_clean_data_invalid_input():
    with pytest.raises(ValueError):
        clean_data("invalid input type")

if __name__ == "__main__":
    pytest.main()
