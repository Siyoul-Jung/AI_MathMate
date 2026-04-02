# import pytest (의존성 제거)
from backend.engine_v2.iipc_validator import IIPCValidator

def run_tests():
    print("🚀 Starting IIPC Reflection Memory Strategy Tests...")
    validator = IIPCValidator(daps_threshold=14.0)
    
    # 1. 특정 문제 데이터 유입 (실패 상황 가정)
    problem_data = {
        "logic_id": "test_geometry_loop",
        "params": {"radius": 10, "center_visible": False}
    }
    
    print("- Testing loop prevention...")
    # 임의로 실패 기록 (모의 검증 실패)
    validator._update_reflection_memory(problem_data, "Logic contradiction")
    
    # 2. 동일한 데이터로 다시 검증 요청
    # _is_redundant_failure가 True를 반환해야 함
    assert validator._is_redundant_failure(problem_data) is True
    print("  [PASS] Redundant logic detected successfully.")
    
    # 3. 다른 데이터로 검증 요청
    print("- Testing new logic exploration...")
    new_problem_data = {
        "logic_id": "test_geometry_loop",
        "params": {"radius": 15, "center_visible": True}
    }
    assert validator._is_redundant_failure(new_problem_data) is False
    print("  [PASS] New logic exploration allowed.")

    # 4. Adaptive Compute Allocation 구조 확인
    print("- Testing adaptive compute allocation structure...")
    assert validator.validate({"test": 1}, 15.0) is True
    print("  [PASS] Adaptive Compute logic check.")
    
    print("\n✅ All IIPC Strategy Tests Passed!")

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as e:
        print(f"\n❌ Test Failed!")
        exit(1)
