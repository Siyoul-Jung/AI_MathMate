import pytest
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from amc_engine.pipeline_manager import ProblemFactory

def test_pipeline_manager_init():
    """Test if Pipeline Manager initializes without error."""
    try:
        manager = ProblemFactory()
        assert manager is not None
    except Exception as e:
        pytest.fail(f"ProblemFactory initialization failed: {e}")

def test_db_existence():
    """Test if necessary databases exist."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "amc_engine", "amc_factory.db")
    assert os.path.exists(db_path), f"Database {db_path} not found"

def test_random_variant_retrieval():
    """Test if we can retrieve a random variant (P01)."""
    manager = ProblemFactory()
    try:
        # Using AIME1, 2025, P01 as test case
        variant = manager.get_random_variant("2025", "AIME1", "P01")
        if variant:
            assert "3_presentation" in variant
            assert "problem_statement" in variant["3_presentation"]
    except Exception as e:
        pytest.fail(f"Random variant retrieval failed: {e}")
