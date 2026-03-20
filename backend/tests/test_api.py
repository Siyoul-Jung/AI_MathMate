import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI MathMate API" in response.text

def test_api_types():
    """Test the /api/types endpoint."""
    # AIME_1 is a known grade for AIME
    response = client.get("/api/types?standard=AIME&grade=AIME_1")
    assert response.status_code == 200
    data = response.json()
    assert "types" in data
    assert isinstance(data["types"], list)

def test_amc_levels_exists():
    """Test if /api/amc/levels/{p_id} exists for P01."""
    response = client.get("/api/amc/levels/P01")
    assert response.status_code == 200
    data = response.json()
    assert "levels" in data
    assert "band" in data

def test_generate_problem_unauthorized_params():
    """Test /api/amc/generate with missing params."""
    response = client.get("/api/amc/generate")
    # FastAPI returns 422 Unprocessable Entity for missing required query params
    assert response.status_code == 422
