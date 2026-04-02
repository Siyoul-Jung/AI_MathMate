import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amc_engine.pipeline_manager import load_solver_dynamically

PROBLEMS = [f"P{i:02d}" for i in range(1, 16)]

@pytest.mark.parametrize("p_id", PROBLEMS)
def test_aime_solver_golden_standard(p_id):
    year, exam = "2025", "AIME1"
    
    # 1. Load Solver
    Solver_cls = load_solver_dynamically(year, exam, p_id)
    assert Solver_cls is not None, f"Failed to load solver {p_id}"
    
    # 2. Check DNA
    dna = getattr(Solver_cls, 'DNA', {})
    required_keys = ["specific_tag", "category", "level", "has_image"]
    for key in required_keys:
        assert key in dna, f"DNA of {p_id} missing key: {key}"
    assert dna["level"] == int(p_id[1:]), f"DNA level mismatch for {p_id}"
    
    # 3. Verify Execution Logic
    seed = Solver_cls.generate_seed()
    assert seed is not None, f"Seed generation failed for {p_id}"
    assert 'expected_t' in seed, f"Seed for {p_id} missing 'expected_t'"
    
    solver = Solver_cls(seed)
    result = solver.execute()
    assert result == seed['expected_t'], f"Execution result {result} != expected {seed['expected_t']} for {p_id}"
    
    # 4. Check Drill Interface
    if hasattr(Solver_cls, 'DRILL_LEVELS'):
        for lv in Solver_cls.DRILL_LEVELS:
            if lv == 3: continue # Usually same as main
            d_seed = Solver_cls.generate_drill_seed(lv)
            assert d_seed is not None, f"Drill seed (LV{lv}) failed for {p_id}"
            assert 'expected_t' in d_seed, f"Drill seed (LV{lv}) for {p_id} missing 'expected_t'"
            
            d_solver = Solver_cls(d_seed)
            d_result = d_solver.execute()
            assert d_result == d_seed['expected_t'], f"Drill LV{lv} execution mismatch for {p_id}"

@pytest.mark.parametrize("p_id", PROBLEMS)
def test_aime_image_generation_crash_check(p_id, tmp_path):
    year, exam = "2025", "AIME1"
    Solver_cls = load_solver_dynamically(year, exam, p_id)
    
    if Solver_cls.DNA.get("has_image"):
        seed = Solver_cls.generate_seed()
        img_path = os.path.join(tmp_path, f"{p_id}_test.png")
        try:
            Solver_cls.generate_image(seed, img_path)
            assert os.path.exists(img_path), f"Image not created for {p_id}"
        except Exception as e:
            pytest.fail(f"Image generation crashed for {p_id}: {str(e)}")
