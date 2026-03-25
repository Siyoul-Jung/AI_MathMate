import pytest
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amc_engine.pipeline_manager import ProblemFactory, load_solver_dynamically

@pytest.fixture
def factory():
    """Fixture to provide a ProblemFactory instance."""
    return ProblemFactory()

def test_p01_solver_logic(factory):
    """
    Verify that the P01 (Logarithm/Sequence) solver correctly 
    calculates the expected answer based on the generated seed.
    """
    year, exam, p_id = "2025", "AIME1", "P01"
    
    # Load solver class dynamically
    Solver_cls = load_solver_dynamically(year, exam, p_id)
    
    # Generate a new variant seed
    seed = Solver_cls.generate_seed()
    
    # Initialize solver with the seed (as payload)
    solver = Solver_cls(seed)
    
    # Execute and check if it matches the expected_t in seed
    result = solver.execute()
    assert result == seed['expected_t'], f"Solver result {result} should match expected {seed['expected_t']}"
    assert isinstance(result, (int, float)), "Result must be numeric"

def test_p02_solver_drill_logic(factory):
    """
    Verify the newly implemented P02 (Area Ratio) drill logic.
    Ensures that drill seeds for LV1 and LV2 are valid.
    """
    year, exam, p_id = "2025", "AIME1", "P02"
    Solver_cls = load_solver_dynamically(year, exam, p_id)
    
    # Test Level 1 Drill Seed
    l1_seed = Solver_cls.generate_drill_seed(1)
    assert 'k' in l1_seed and 'area_small' in l1_seed
    assert l1_seed['expected_t'] == float(l1_seed['area_small'] * (l1_seed['k']**2))

    # Test Level 2 Drill Seed
    l2_seed = Solver_cls.generate_drill_seed(2)
    assert 'quad_area' in l2_seed
    assert l2_seed['expected_t'] == l2_seed['total_area']

def test_p03_solver_determinism(factory):
    """
    Ensures that given the same seed, the solver produces the same result.
    This is critical for the zero-hallucination architecture.
    """
    year, exam, p_id = "2025", "AIME1", "P03"
    Solver_cls = load_solver_dynamically(year, exam, p_id)
    seed = Solver_cls.generate_seed()
    
    solver1 = Solver_cls(seed)
    solver2 = Solver_cls(seed)
    
    assert solver1.execute() == solver2.execute(), "Solver execution must be deterministic"

def test_invalid_problem_id(factory):
    """Verify that requesting an invalid problem ID raises an appropriate error."""
    with pytest.raises(FileNotFoundError):
        load_solver_dynamically("2025", "AIME1", "P999")
